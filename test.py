from pathlib import PurePosixPath
from unittest import TestCase

from main import parse_path, ParsedLaunchPath, starts_with_dot, is_launch_file


class TestParsePath(TestCase):
    def test_no_launch(self):
        self.assertRaises(ValueError, lambda: parse_path(PurePosixPath('file.launch')))

    def test_two_launch(self):
        self.assertRaises(ValueError, lambda: parse_path(PurePosixPath('simulator/launch/include/launch/file.launch')))

    def test_starts_with_launch(self):
        self.assertRaises(ValueError, lambda: parse_path(PurePosixPath('launch/simulator/launch/file.launch')))

    def test_ends_with_launch(self):
        self.assertRaises(ValueError, lambda: parse_path(PurePosixPath('simulator/launch')))

    def test_basic(self):
        self.assertEqual(ParsedLaunchPath('simulator', 'file.launch'), parse_path(PurePosixPath('simulator/launch/file.launch')))

    def test_basic_xml(self):
        self.assertEqual(ParsedLaunchPath('simulator', 'file.launch.xml'), parse_path(PurePosixPath('simulator/launch/file.launch.xml')))

    def test_other_extension(self):
        self.assertEqual(ParsedLaunchPath('simulator', 'file.dat'), parse_path(PurePosixPath('simulator/launch/file.dat')))

    def test_extended_path(self):
        self.assertEqual(ParsedLaunchPath('simulator', 'file.launch'), parse_path(PurePosixPath('~/ros/workspace/simulator/launch/file.launch')))


class TestStartsWithDot(TestCase):
    def test_file(self):
        self.assertTrue(starts_with_dot(PurePosixPath('.file.launch.xml')))
        self.assertTrue(starts_with_dot(PurePosixPath('.launch')))

        self.assertFalse(starts_with_dot(PurePosixPath('file.launch')))

    def test_file_and_directory(self):
        self.assertTrue(starts_with_dot(PurePosixPath('.hidden/launch/file.launch')))
        self.assertTrue(starts_with_dot(PurePosixPath('hidden/.launch/file.launch')))

        self.assertFalse(starts_with_dot(PurePosixPath('hidden/launch/file.launch')))
        self.assertFalse(starts_with_dot(PurePosixPath('./launch/file.launch')))


class TestIsLaunchFile(TestCase):
    def test_launch(self):
        self.assertTrue(is_launch_file(PurePosixPath('simulator/launch/file.launch')))

    def test_launch_xml(self):
        self.assertTrue(is_launch_file(PurePosixPath('simulator/launch/file.launch.xml')))

    def test_xml(self):
        self.assertFalse(is_launch_file(PurePosixPath('simulator/launch/file.xml')))

    def test_other_extension(self):
        self.assertFalse(is_launch_file(PurePosixPath('simulator/launch/file.md')))

    def test_other_location(self):
        self.assertTrue(is_launch_file(PurePosixPath('simulator/file.launch')))
        self.assertTrue(is_launch_file(PurePosixPath('file.launch')))
