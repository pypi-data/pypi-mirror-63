#! /usr/bin/env python
# remarshal, a utility to convert between serialization formats.
# Copyright (c) 2014, 2015, 2016, 2017, 2018, 2019, 2020 D. Bohdan
# License: MIT

from .context import remarshal
import collections
import datetime
import errno
import os
import os.path
import re
import sys
import tempfile
import unittest
import cbor2

TEST_PATH = os.path.dirname(os.path.realpath(__file__))
PYTHON_3 = True
try:
    unicode
    PYTHON_3 = False
except NameError:
    pass


def test_file_path(filename):
    path_list = [TEST_PATH]
    if re.match(r'example\.(json|msgpack|toml|yaml|cbor)$', filename):
        path_list.append('..')
    path_list.append(filename)
    return os.path.join(*path_list)


def readFile(filename, binary=False):
    with open(test_file_path(filename), 'rb') as f:
        content = f.read()
        if not binary:
            content = content.decode('utf-8')
    return content


def tomlSignature(data):
    '''A lossy representation for TOML example data for comparison.'''
    def strip_more(line):
        return re.sub(r' *#.*$', '', line.strip()).replace(' ', '')

    def f(lst):
        def q(line):
            return (
                line.startswith('#') or
                line == u'' or
                line == u']' or
                re.match(r'^".*",?$', line) or
                re.match(r'^hosts', line)
            )
        return sorted(
            [strip_more(line) for line in lst if not q(strip_more(line))]
        )

    return f(data.split("\n"))


def sorted_dict(d):
    return collections.OrderedDict(sorted(d.items()))

def transformDateToIso(col):
    return col.isoformat() if isinstance(col, datetime.datetime) else col

class TestRemarshal(unittest.TestCase):

    def tempFilename(self):
        fd, temp_filename = tempfile.mkstemp()
        os.close(fd)
        self.temp_files.append(temp_filename)
        return temp_filename

    def assertCborSame(self, output, reference):

        # To date, Python's CBOR libraries don't support encoding to
        # canonical-form CBOR, so we have to parse and deep-compare.
        output_dec = cbor2.loads(output)
        reference_dec = cbor2.loads(reference)
        self.assertEqual(output_dec, reference_dec)

    def convertAndRead(
        self,
        input,
        input_format,
        output_format,
        wrap=None,
        unwrap=None,
        indent_json=True,
        yaml_options={},
        ordered=False,
        binary=False,
        transform=None,
    ):
        output_filename = self.tempFilename()
        remarshal.remarshal(
            test_file_path(input),
            output_filename,
            input_format,
            output_format,
            wrap=wrap,
            unwrap=unwrap,
            indent_json=indent_json,
            yaml_options=yaml_options,
            ordered=ordered,
            transform=transform
        )
        return readFile(output_filename, binary)

    def setUp(self):
        self.maxDiff = None
        self.temp_files = []

    def tearDown(self):
        for filename in self.temp_files:
            os.remove(filename)

    def test_json2json(self):
        output = self.convertAndRead('example.json', 'json', 'json')
        reference = readFile('example.json')
        self.assertEqual(output, reference)

    def test_msgpack2msgpack(self):
        output = self.convertAndRead(
            'example.msgpack',
            'msgpack',
            'msgpack',
            binary=True,
            ordered=True,
        )
        reference = readFile('example.msgpack', binary=True)
        self.assertEqual(output, reference)

    def test_toml2toml(self):
        output = self.convertAndRead('example.toml', 'toml', 'toml')
        reference = readFile('example.toml')
        self.assertEqual(tomlSignature(output), tomlSignature(reference))

    def test_yaml2yaml(self):
        output = self.convertAndRead('example.yaml', 'yaml', 'yaml')
        reference = readFile('example.yaml')
        self.assertEqual(output, reference)

    def test_cbor2cbor(self):
        output = self.convertAndRead('example.cbor', 'cbor', 'cbor', binary=True)
        reference = readFile('example.cbor', binary=True)
        self.assertCborSame(output, reference)

    def test_json2msgpack(self):
        def patch(x):
            x['owner']['dob'] = datetime.datetime(1979, 5, 27, 7, 32)
            return x

        output = self.convertAndRead(
            'example.json',
            'json',
            'msgpack',
            binary=True,
            ordered=True,
            transform=patch,
        )
        reference = readFile('example.msgpack', binary=True)
        self.assertEqual(output, reference)

    @unittest.skipUnless(PYTHON_3, 'requires Python 3')
    def test_json2cbor(self):
        def patch(x):
            x['owner']['dob'] = datetime.datetime(1979, 5, 27, 7, 32, 0, 0, datetime.timezone.utc)
            return x

        output = self.convertAndRead(
            'example.json',
            'json',
            'cbor',
            binary=True,
            ordered=True,
            transform=patch,
        )

        reference = readFile('example.cbor', binary=True)
        self.assertCborSame(output, reference)

    def test_json2toml(self):
        output = self.convertAndRead('example.json', 'json', 'toml')
        reference = readFile('example.toml')
        output_sig = tomlSignature(output)
        # The date in 'example.json' is a string.
        reference_sig = tomlSignature(
            reference.replace(
                '1979-05-27T07:32:00Z',
                '"1979-05-27T07:32:00+00:00"'
            )
        )
        self.assertEqual(output_sig, reference_sig)

    def test_json2yaml(self):
        output = self.convertAndRead('example.json', 'json', 'yaml')
        reference = readFile('example.yaml')
        # The date in 'example.json' is a string.
        reference_patched = reference.replace(
            '1979-05-27 07:32:00+00:00',
            "'1979-05-27T07:32:00+00:00'"
        )
        self.assertEqual(output, reference_patched)

    def test_msgpack2json(self):
        output = self.convertAndRead('example.msgpack', 'msgpack', 'json')
        reference = readFile('example.json')
        self.assertEqual(output, reference)

    def test_msgpack2toml(self):
        output = self.convertAndRead('example.msgpack', 'msgpack', 'toml')
        reference = readFile('example.toml')
        self.assertEqual(tomlSignature(output), tomlSignature(reference))

    def test_msgpack2yaml(self):
        output = self.convertAndRead('example.msgpack', 'msgpack', 'yaml')
        reference = readFile('example.yaml')
        self.assertEqual(output, reference)

    def test_msgpack2cbor(self):
        output = self.convertAndRead(
            'example.msgpack', 'msgpack', 'cbor',
            binary=True,
        )
        reference = readFile('example.cbor', binary=True)
        self.assertCborSame(output, reference)

    def test_toml2json(self):
        output = self.convertAndRead('example.toml', 'toml', 'json')
        reference = readFile('example.json')
        self.assertEqual(output, reference)

    def test_toml2msgpack(self):
        output = self.convertAndRead(
            'example.toml',
            'toml',
            'msgpack',
            binary=True,
            transform=lambda col: remarshal.traverse(
                col,
                dict_callback=sorted_dict
            ),
        )
        reference = readFile('example.msgpack', binary=True)
        self.assertEqual(output, reference)

    def test_toml2yaml(self):
        output = self.convertAndRead('example.toml', 'toml', 'yaml')
        reference = readFile('example.yaml')
        self.assertEqual(output, reference)

    def test_toml2cbor(self):
        output = self.convertAndRead(
            'example.toml', 'toml', 'cbor',
            binary=True,
        )
        reference = readFile('example.cbor', binary=True)
        self.assertCborSame(output, reference)

    def test_yaml2json(self):
        output = self.convertAndRead('example.yaml', 'yaml', 'json')
        reference = readFile('example.json')
        self.assertEqual(output, reference)

    def test_yaml2msgpack(self):
        output = self.convertAndRead(
            'example.yaml',
            'yaml',
            'msgpack',
            ordered=True,
            binary=True,
        )
        reference = readFile('example.msgpack', binary=True)
        self.assertEqual(output, reference)

    def test_yaml2toml(self):
        output = self.convertAndRead('example.yaml', 'yaml', 'toml')
        reference = readFile('example.toml')
        self.assertEqual(tomlSignature(output), tomlSignature(reference))

    def test_yaml2cbor(self):
        output = self.convertAndRead(
            'example.yaml', 'yaml', 'cbor',
            binary=True,
        )
        reference = readFile('example.cbor', binary=True)
        self.assertCborSame(output, reference)

    def test_cbor2json(self):
        output = self.convertAndRead('example.cbor', 'cbor', 'json')
        reference = readFile('example.json')
        self.assertEqual(output, reference)

    def test_cbor2toml(self):
        output = self.convertAndRead('example.cbor', 'cbor', 'toml')
        reference = readFile('example.toml')
        output_sig = tomlSignature(output)
        reference_sig = tomlSignature(reference)
        self.assertEqual(output_sig, reference_sig)

    def test_cbor2yaml(self):
        output = self.convertAndRead('example.cbor', 'cbor', 'yaml')
        reference = readFile('example.yaml')
        self.assertEqual(output, reference)

    def test_cbor2msgpack(self):
        output = self.convertAndRead(
            'example.cbor',
            'cbor',
            'msgpack',
            binary=True,
            ordered=True,
            transform=lambda col: remarshal.traverse(
                col,
                dict_callback=sorted_dict
            ),
        )
        reference = readFile('example.msgpack', binary=True)
        self.assertEqual(output, reference)

    def test_missing_wrap(self):
        with self.assertRaises(ValueError) as context:
            output = self.convertAndRead('array.json', 'json', 'toml')

    def test_wrap(self):
        output = self.convertAndRead('array.json', 'json', 'toml',
                                     wrap='data')
        reference = readFile('array.toml')
        self.assertEqual(output, reference)

    def test_unwrap(self):
        output = self.convertAndRead('array.toml', 'toml', 'json',
                                     unwrap='data',
                                     indent_json=None)
        reference = readFile('array.json')
        self.assertEqual(output, reference)

    def test_malformed_json(self):
        with self.assertRaises(ValueError) as context:
            self.convertAndRead('garbage', 'json', 'yaml')

    def test_malformed_toml(self):
        with self.assertRaises(ValueError) as context:
            self.convertAndRead('garbage', 'toml', 'yaml')

    def test_malformed_yaml(self):
        with self.assertRaises(ValueError) as context:
            self.convertAndRead('garbage', 'yaml', 'json')

    @unittest.skipUnless(PYTHON_3, 'requires Python 3')
    def test_binary_to_json(self):
        with self.assertRaises(ValueError) as context:
            self.convertAndRead('bin.msgpack', 'msgpack', 'json')
        with self.assertRaises(ValueError) as context:
            self.convertAndRead('bin.yml', 'yaml', 'json')

    @unittest.skipUnless(PYTHON_3, 'requires Python 3')
    def test_binary_to_msgpack(self):
        self.convertAndRead('bin.yml', 'yaml', 'msgpack', binary=True)

    @unittest.skipUnless(PYTHON_3, 'requires Python 3')
    def test_binary_to_toml(self):
        with self.assertRaises(ValueError) as context:
            self.convertAndRead('bin.msgpack', 'msgpack', 'toml')
        with self.assertRaises(ValueError) as context:
            self.convertAndRead('bin.yml', 'yaml', 'toml')

    @unittest.skipUnless(PYTHON_3, 'requires Python 3')
    def test_binary_to_yaml(self):
        self.convertAndRead('bin.msgpack', 'msgpack', 'yaml')

    @unittest.skipUnless(PYTHON_3, 'requires Python 3')
    def test_binary_to_cbor(self):
        self.convertAndRead('bin.msgpack', 'msgpack', 'cbor', binary=True)

    def test_yaml_style_default(self):
        output = self.convertAndRead('long-line.json', 'json', 'yaml')
        reference = readFile('long-line-default.yaml')
        self.assertEqual(output, reference)

    def test_yaml_style_single_quote(self):
        output = self.convertAndRead(
            'long-line.json',
            'json',
            'yaml',
            yaml_options={'default_style': "'"}
        )
        reference = readFile('long-line-single-quote.yaml')
        self.assertEqual(output, reference)

    def test_yaml_style_double_quote(self):
        output = self.convertAndRead(
            'long-line.json',
            'json',
            'yaml',
            yaml_options={'default_style': '"'}
        )
        reference = readFile('long-line-double-quote.yaml')
        self.assertEqual(output, reference)

    def test_yaml_style_pipe(self):
        output = self.convertAndRead(
            'long-line.json',
            'json',
            'yaml',
            yaml_options={'default_style': '|'}
        )
        reference = readFile('long-line-pipe.yaml')
        self.assertEqual(output, reference)

    def test_yaml_style_gt(self):
        output = self.convertAndRead(
            'long-line.json',
            'json',
            'yaml',
            yaml_options={'default_style': '>'}
        )
        reference = readFile('long-line-gt.yaml')
        self.assertEqual(output, reference)

    def test_argv0_to_format(self):
        def test_format_string(s):
            for from_str in 'json', 'toml', 'yaml':
                for to_str in 'json', 'toml', 'yaml':
                    found, from_parsed, to_parsed = remarshal.argv0_to_format(
                        s.format(from_str, to_str)
                    )
                    self.assertEqual(
                        (found, from_parsed, to_parsed),
                        (found, from_str, to_str)
                    )

        test_format_string('{0}2{1}')
        test_format_string('{0}2{1}.exe')
        test_format_string('{0}2{1}-script.py')

    def test_format_detection(self):
        ext_to_fmt = {
            'json': 'json',
            'toml': 'toml',
            'yaml': 'yaml',
            'yml': 'yaml',
        }

        for from_ext in ext_to_fmt.keys():
            for to_ext in ext_to_fmt.keys():
                args = remarshal.parse_command_line([
                    sys.argv[0],
                    'input.' + from_ext,
                    'output.' + to_ext
                ])

                self.assertEqual(args.input_format, ext_to_fmt[from_ext])
                self.assertEqual(args.output_format, ext_to_fmt[to_ext])

    def test_format_detection_failure_input_stdin(self):
        with self.assertRaises(SystemExit) as cm:
            remarshal.parse_command_line([sys.argv[0], '-'])
        self.assertEqual(cm.exception.code, 2)

    def test_format_detection_failure_input_txt(self):
        with self.assertRaises(SystemExit) as cm:
            remarshal.parse_command_line([sys.argv[0], 'input.txt'])
        self.assertEqual(cm.exception.code, 2)

    def test_format_detection_failure_output_txt(self):
        with self.assertRaises(SystemExit) as cm:
            remarshal.parse_command_line([
                sys.argv[0],
                'input.json',
                'output.txt'
            ])
        self.assertEqual(cm.exception.code, 2)

    def test_run_no_args(self):
        with self.assertRaises(SystemExit) as cm:
            remarshal.run([sys.argv[0]])
        self.assertEqual(cm.exception.code, 2)

    def test_run_help(self):
        with self.assertRaises(SystemExit) as cm:
            remarshal.run([sys.argv[0], '--help'])
        self.assertEqual(cm.exception.code, 0)

    def test_run_no_input_file(self):
        with self.assertRaises(IOError) as cm:
            args = [
                sys.argv[0],
                '-if',
                'json',
                '-of',
                'json',
                'fake-input-file-that-almost-certainly-doesnt-exist-2382'
            ]
            remarshal.run(args)
        self.assertEqual(cm.exception.errno, errno.ENOENT)

    def test_run_no_output_dir(self):
        with self.assertRaises(IOError) as cm:
            args = [
                sys.argv[0],
                '-if',
                'json',
                '-of',
                'json',
                '-o',
                'this_path/almost-certainly/doesnt-exist-5836',
                test_file_path('example.json')
            ]
            remarshal.run(args)
        self.assertEqual(cm.exception.errno, errno.ENOENT)

    def test_run_no_output_format(self):
        with self.assertRaises(SystemExit) as cm:
            remarshal.run([sys.argv[0], test_file_path('array.toml')])
        self.assertEqual(cm.exception.code, 2)

    def test_ordered_simple(self):
        for from_ in 'json', 'toml', 'yaml':
            for to in 'json', 'toml', 'yaml':
                output = self.convertAndRead(
                    'order.' + from_,
                    from_,
                    to,
                    ordered=True
                )
                reference = readFile('order.' + to)
                self.assertEqual(output, reference)

    def test_ordered_yaml2yaml(self):
        output = self.convertAndRead(
            'example.yaml',
            'yaml',
            'yaml',
            ordered=True
        )
        reference = readFile('example.yaml')
        self.assertEqual(output, reference)


if __name__ == '__main__':
    unittest.main()
