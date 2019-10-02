import os
import shutil
import unittest
import subprocess

__author__ = 'Akshat Bajaj'
__date__ = '2019/03/01'

class RemoteTest(unittest.TestCase):

    def test_remote(self):
        process = subprocess.run(['surround', 'store', 'remote'], encoding='utf-8', stdout=subprocess.PIPE)
        self.assertEqual(process.stdout, "error: not a surround project\n")

        process = subprocess.run(['surround', 'init', './', '-p', 'temp', '-d', 'temp', '-w', 'no'], encoding='utf-8', stdout=subprocess.PIPE)
        self.assertRegex(process.stdout, 'info: project created at .*temp\\n')

        is_temp = os.path.isdir(os.path.join(os.getcwd() + "/temp"))
        self.assertEqual(is_temp, True)

        process = subprocess.run(['surround', 'store', 'remote'], encoding='utf-8', stdout=subprocess.PIPE, cwd='temp')
        self.assertEqual(process.stdout, "info: no remote found\n")

    def test_remote_add(self):
        process = subprocess.run(['surround', 'init', './', '-p', 'temp', '-d', 'temp', '-w', 'no'], encoding='utf-8', stdout=subprocess.PIPE)
        self.assertRegex(process.stdout, 'info: project created at .*temp\\n')

        is_temp = os.path.isdir(os.path.join(os.getcwd() + "/temp"))
        self.assertEqual(is_temp, True)

        process = subprocess.run(['surround', 'store', 'remote', '-a', '-n', 'data', '-u', os.getcwd()], encoding='utf-8', stdout=subprocess.PIPE, cwd='temp')

        process = subprocess.run(['surround', 'store', 'remote'], encoding='utf-8', stdout=subprocess.PIPE, cwd='temp')
        self.assertEqual(process.stdout, "data\n")

        process = subprocess.run(['surround', 'store', 'remote', '-v'], encoding='utf-8', stdout=subprocess.PIPE, cwd='temp')
        self.assertEqual(process.stdout, "data: " + os.getcwd() + "\n")

    def tearDown(self):
        # Remove residual files
        shutil.rmtree('temp')
