import unittest
import os
import yaml

from surround.data import Metadata

class TestMetadata(unittest.TestCase):
    def setUp(self):
        self.test_data = {
            'version': 'v0.1',
            'summary': {
                'title': 'test_title',
                'description': 'test_description',
            },
            'manifests': [
                {
                    'path': 'test.txt',
                    'description': 'test_description',
                    'types': ['Text'],
                    'formats': ['text/plain'],
                    'language': 'en'
                }
            ]
        }

        with open("test-metadata.yaml", "w+") as f:
            yaml.dump(self.test_data, f)

    def tearDown(self):
        os.unlink("test-metadata.yaml")

        if os.path.exists('test-save-to-file.yaml'):
            os.unlink('test-save-to-file.yaml')

        if os.path.exists('test-file.txt'):
            os.unlink('test-file.txt')

    def test_create(self):
        metadata = Metadata(version='v0.2')
        self.assertEqual(metadata.get_property("version"), "v0.2")

    def test_load_from_path(self):
        metadata = Metadata()
        metadata.load_from_path('test-metadata.yaml')

        self.assertEqual(metadata["summary"]["title"], "test_title")
        self.assertEqual(metadata["manifests"][0]["path"], "test.txt")

    def test_load_from_path_invalid(self):
        metadata = Metadata()

        with self.assertRaises(FileNotFoundError):
            metadata.load_from_path('test-metadata-nope.yaml')

    def test_load_from_data(self):
        metadata = Metadata()
        metadata.load_from_data("version: v0.1")

        self.assertEqual(metadata['version'], 'v0.1')

    def test_load_from_data_invalid(self):
        metadata = Metadata()

        with self.assertRaises(yaml.YAMLError):
            metadata.load_from_data("{{{}} invalid")

    def test_save_to_data(self):
        metadata = Metadata()
        metadata.set_property('version', 'v0.1')
        metadata.set_property('summary', {'title': 'test_title'})

        data = metadata.save_to_data()

        metadata = Metadata()
        metadata.load_from_data(data)
        self.assertEqual(metadata['version'], 'v0.1')
        self.assertEqual(metadata['summary']['title'], 'test_title')

    def test_save_to_file(self):
        metadata = Metadata()
        metadata.set_property('version', 'v0.1')
        metadata.set_property('summary', {'title': 'test_title'})

        metadata.save_to_path('test-save-to-file.yaml')

        metadata = Metadata()
        metadata.load_from_path('test-save-to-file.yaml')

        self.assertEqual(metadata['version'], 'v0.1')
        self.assertEqual(metadata['summary']['title'], 'test_title')

        os.unlink('test-save-to-file.yaml')

    def test_get_property(self):
        metadata = Metadata()
        metadata.set_property('version', 'v0.1')
        metadata.set_property('summary', {'title': 'test_title'})

        self.assertEqual(metadata.get_property("version"), 'v0.1')
        self.assertDictEqual(metadata.get_property('summary'), {'title': 'test_title'})

    def test_nested_get_property(self):
        metadata = Metadata()
        metadata.set_property('version', 'v0.1')
        metadata.set_property('summary', {'title': 'test_title', 'description': 'test_description'})

        self.assertEqual(metadata.get_property("summary.title"), metadata["summary"]["title"])
        self.assertEqual(metadata.get_property("summary.description"), metadata["summary"]["description"])
        self.assertEqual(metadata.get_property('summary.title'), 'test_title')
        self.assertEqual(metadata.get_property('summary.description'), 'test_description')

    def test_set_property(self):
        metadata = Metadata()
        metadata.set_property('version', 'v0.1')
        metadata.set_property('summary', {'title': 'test_title'})

        metadata.set_property('info', 'more info')
        metadata.set_property('schema', {'data': 'int'})

        self.assertEqual(metadata['version'], 'v0.1')
        self.assertEqual(metadata['summary']['title'], 'test_title')
        self.assertEqual(metadata['info'], 'more info')
        self.assertEqual(metadata['schema'], {'data': 'int'})

    def test_set_nested_property(self):
        metadata = Metadata()
        metadata.set_property('version', 'v0.1')
        metadata.set_property('summary', {})
        metadata.set_property("summary.title", 'test_title')

        self.assertIn('title', metadata['summary'])
        self.assertEqual(metadata['summary']['title'], 'test_title')

    def test_modify_property(self):
        metadata = Metadata()
        metadata.set_property('version', 'v0.1')
        metadata.set_property('summary', {'title': 'test_title'})

        metadata.set_property('version', 'v0.2')
        self.assertEqual(metadata['version'], 'v0.2')

    def test_modify_nested_property(self):
        metadata = Metadata()
        metadata.set_property('version', 'v0.1')
        metadata.set_property('summary', {'title': 'test_title'})

        metadata.set_property('summary.title', 'another_test_title')
        self.assertEqual(metadata['summary']['title'], 'another_test_title')

    def test_get_property_via_subscript(self):
        metadata = Metadata()
        metadata.set_property('version', 'v0.1')
        metadata.set_property('summary', {'title': 'test_title'})

        self.assertEqual(metadata['version'], 'v0.1')
        self.assertEqual(metadata['summary']['title'], 'test_title')

    def test_generate_from_directory(self):
        metadata = Metadata()
        metadata.generate_from_directory('.')

        self.assertIn('Text', metadata['summary']['types'])
        self.assertIn('Collection', metadata['summary']['types'])
        self.assertIn('text/plain', metadata['summary']['formats'])

    def test_generate_from_file(self):
        with open("test-file.txt", "w+") as f:
            f.write("This is a test data file")

        metadata = Metadata()
        metadata.generate_from_file('test-file.txt')

        self.assertIn('Text', metadata['summary']['types'])
        self.assertIn('text/plain', metadata['summary']['formats'])

        os.unlink('test-file.txt')
