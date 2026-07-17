#!/usr/bin/env python3

import unittest
from random import randint
import sys, os
import subprocess as sp
from importlib import import_module
from unittest.mock import mock_open, patch, call

'''
ASSIGNMENT 2 CHECK SCRIPT
Winter 2023
Author: Eric Brauer eric.brauer@senecacollege.ca

Description:
TestAfter .. TestDBDA all are testing functions inside students' code. 
TestFinal will run the code as a subprocess and evaluate the std.output.

The precise requirements of each student-created function are specified elsewhere.

The script assumes that the student's filename is named 'assignment2.py' and exists in the same directory as this check script.

NOTE: Feel free to _fork_ and modify this script to suit needs. I will try to fix any issues that arise but this script is provided as-is, with no obligation of warranty or support.
'''

class TestModuleRestriction(unittest.TestCase):
    "no modules apart from allowed are being imported"
    
    def setUp(self):
        self.filename = 'assignment2.py'
        self.pypath = sys.executable
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
        try:
            self.a2 = import_module(self.filename.split('.')[0])
        except ModuleNotFoundError:
            print("Cannot find a function inside your assignment2.py. Do not rename or delete any of the required functions.")
    
    def test_unallowed_module(self):
        "you have imported a prohibited module"
        verboten = ['psutil']
        allowed = ["sys", "subprocess", "argparse", "os"]
        for mod in verboten:
            if mod in sys.modules:
                raise AssertionError(f'You have imported a prohibited module.'
                    f'module {mod} is not allowed. Review the Wiki' 
                    ' instructions again.')


class TestPercent(unittest.TestCase):
    "percent_to_graph is working"
    
    def setUp(self):
        self.filename = 'assignment2.py'
        self.pypath = sys.executable
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
        try:
            self.a2 = import_module(self.filename.split('.')[0])
        except ModuleNotFoundError:
            print("Cannot find a function inside your assignment2.py. Do not rename or delete any of the required functions.")
    
    def test_percent(self):
        "percent_to_graph returns correct '##    ' format"
        percent_list = [33, 56, 70, 63, 89]
        max_list = [10, 15, 20, 30, 80]
        for i in range(0, (len(percent_list)-1)):
            given = self.a2.percent_to_graph((percent_list[i]/100), max_list[i])  # pcnt is 0.0 - 1.0
            inv_pcnt = 100 - percent_list[i]  # to get spaces rather than symbols
            num_spcs = round((max_list[i] * inv_pcnt) / 100) 
            expected = ' ' * num_spcs
            error_msg = "The output of percent_to_graph() with the argument " + str(percent_list[i]) + " is returning the wrong value"
            self.assertIn(expected, given, error_msg)
            self.assertEqual(max_list[i], len(given), error_msg)


class TestMemFuncs(unittest.TestCase):
    "get_sys_mem and get_avail_mem are working"

    mem1 = f'32{randint(0,9)}93367'
    mem2 = f'191{randint(0,9)}640' 
    mem3 = f'25{randint(0,9)}24192'

    data = (f'MemTotal:       {mem1} kB\n'
            f'MemFree:         {mem2} kB\n'
            f'MemAvailable:   {mem3} kB\n'
            'Buffers:         1908176 kB\n'
            'Cached:         20887140 kB\n'
            'SwapCached:            0 kB\n'
            'Active:          8902796 kB\n'
            'Inactive:       17753404 kB\n'
            'Active(anon):      68408 kB\n'
            'Inactive(anon):  4382760 kB')

    def setUp(self):
        self.filename = 'assignment2.py'
        self.pypath = sys.executable
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
        try:
            self.a2 = import_module(self.filename.split('.')[0])
        except ModuleNotFoundError:
            print("Cannot find a function inside your assignment2.py. Do not rename or delete any of the required functions.")

    def test_meminfo_total(self):
        error = ('ERROR: not opening meminfo for memory usage. Use open()'
                 ' and the arguments "/proc/meminfo", "r". ')
        m = mock_open(read_data=self.data)
        with patch('builtins.open', m, create=True):
            given = self.a2.get_sys_mem()
            expected = int(self.mem1)
            self.assertEqual(given, expected, error)
            self.assertEqual(m.call_count, 1, error)
            m.assert_has_calls([call('/proc/meminfo', 'r')])

    def test_meminfo_avail(self):
        error = ('ERROR: not opening meminfo for memory usage. Use open()'
                 ' and the arguments "/proc/meminfo", "r". ')
        m = mock_open(read_data=self.data)
        with patch('builtins.open', m, create=True):
            given = self.a2.get_avail_mem()
            expected = int(self.mem3)
            self.assertEqual(given, expected, error)
            self.assertEqual(m.call_count, 1, error)
            m.assert_has_calls([call('/proc/meminfo', 'r')])


class TestParseArgs(unittest.TestCase):
    "parse_command_args is working"

    def setUp(self):
        self.filename = 'assignment2.py'
        self.pypath = sys.executable
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
        try:
            self.a2 = import_module(self.filename.split('.')[0])
        except ModuleNotFoundError:
            print("Cannot find a function inside your assignment2.py. Do not rename or delete any of the required functions.")

    def test_argparse_help(self):
        "assignment2.py -h returns the required options"
        p = sp.Popen(['/usr/bin/python3', self.filename, '-h'], stdout=sp.PIPE, stdin=sp.PIPE, stderr=sp.PIPE)
        stdout, err = p.communicate()
        # Fail test if process returns a no zero exit status
        return_code = p.wait()
        error_output = 'Output of `assignment2.py -h` doesn\'t match what\'s expected. Make sure you\'ve added an option!)'
        expected_out = ["[-h]", "[-H]", "[-l LENGTH]", "[program]"]
        for string in expected_out:
            self.assertIn(string, stdout.decode('utf-8'), msg=error_output)


class TestPidList(unittest.TestCase):
    "pids_of_prog is working"

    def setUp(self):
        self.filename = 'assignment2.py'
        self.pypath = sys.executable
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
        try:
            self.a2 = import_module(self.filename.split('.')[0])
        except ModuleNotFoundError:
            print("Cannot find a function inside your assignment2.py. Do not rename or delete any of the required functions.")

    def test_pids(self):
        error = 'Error: use os.popen to the call the "pidof" command. Use .read() to get the output. Return a list'
        pid_out = '197592 197549 197432 197417 165748 165718 165690 165669 165649 165623 165621 165620 165615'
        expected = pid_out.split()
        with patch.object(os, 'popen') as mock_popen:
            mock_popen().read.return_value = pid_out
            given = self.a2.pids_of_prog('code')
            self.assertEqual(given, expected, error)  
            self.assertEqual(mock_popen().read.call_count, 1, error)


class TestPidMem(unittest.TestCase):
    "get_mem_of_pid is working"

    mem = 184

    data = ('2c4bfffff000-2c5000000000 ---p 00000000 00:00 0' 
            'Size:           16777220 kB\n'
            'KernelPageSize:        4 kB\n'
            'MMUPageSize:           4 kB\n'
            'Rss:                  80 kB\n'
            'Pss:                   0 kB\n'
            'Shared_Clean:          0 kB\n'
            'Shared_Dirty:          0 kB\n'
            'Private_Clean:         0 kB\n'
            'Private_Dirty:         0 kB\n'
            'Referenced:            0 kB\n'
            'Anonymous:             0 kB\n'
            'LazyFree:              0 kB\n'
            'AnonHugePages:         0 kB\n'
            'ShmemPmdMapped:        0 kB\n'
            'FilePmdMapped:         0 kB\n'
            'Shared_Hugetlb:        0 kB\n'
            'Private_Hugetlb:       0 kB\n'
            'Swap:                  0 kB\n'
            'SwapPss:               0 kB\n'
            'Locked:                0 kB\n'
            'THPeligible:    0\n'
            'ProtectionKey:         0\n'
            'VmFlags: mr mw me sd \n'
            '3e1c00000000-3e1c00201000 ---p 00000000 00:00 0 \n'
            'Size:               2052 kB\n'
            'KernelPageSize:        4 kB\n'
            'MMUPageSize:           4 kB\n'
            'Rss:                   0 kB\n'
            'Pss:                   0 kB\n'
            'Shared_Clean:          0 kB\n'
            'Shared_Dirty:          0 kB\n'
            'Private_Clean:         0 kB\n'
            'Private_Dirty:         0 kB\n'
            'Referenced:            0 kB\n'
            'Anonymous:             0 kB\n'
            'LazyFree:              0 kB\n'
            'AnonHugePages:         0 kB\n'
            'ShmemPmdMapped:        0 kB\n'
            'FilePmdMapped:         0 kB\n'
            'Shared_Hugetlb:        0 kB\n'
            'Private_Hugetlb:       0 kB\n'
            'Swap:                  0 kB\n'
            'SwapPss:               0 kB\n'
            'Locked:                0 kB\n'
            'THPeligible:    0\n'
            'ProtectionKey:         0\n'
            'VmFlags: mr mw me sd \n'
            '3e1c00201000-3e1c00202000 rw-p 00000000 00:00 0 \n'
            'Size:                  4 kB\n'
            'KernelPageSize:        4 kB\n'
            'MMUPageSize:           4 kB\n'
            'Rss:                   4 kB\n'
            'Pss:                   4 kB\n'
            'Shared_Clean:          0 kB\n'
            'Shared_Dirty:          0 kB\n'
            'Private_Clean:         0 kB\n'
            'Private_Dirty:         4 kB\n'
            'Referenced:            4 kB\n'
            'Anonymous:             4 kB\n'
            'LazyFree:              0 kB\n'
            'AnonHugePages:         0 kB\n'
            'ShmemPmdMapped:        0 kB\n'
            'FilePmdMapped:         0 kB\n'
            'Shared_Hugetlb:        0 kB\n'
            'Private_Hugetlb:       0 kB\n'
            'Swap:                  0 kB\n'
            'SwapPss:               0 kB\n'
            'Locked:                0 kB\n'
            'THPeligible:    0\n'
            'ProtectionKey:         0\n'
            'VmFlags: rd wr mr mw me ac sd \n'
            '3e1c00202000-3e1c0020c000 ---p 00000000 00:00 0 \n'
            'Size:                 40 kB\n'
            'KernelPageSize:        4 kB\n'
            'MMUPageSize:           4 kB\n'
            'Rss:                 100 kB\n'
            'Pss:                   0 kB\n'
            'Shared_Clean:          0 kB\n'
            'Shared_Dirty:          0 kB\n'
            'Private_Clean:         0 kB\n'
            'Private_Dirty:         0 kB\n'
            'Referenced:            0 kB\n'
            'Anonymous:             0 kB\n'
            'LazyFree:              0 kB\n'
            'AnonHugePages:         0 kB\n'
            'ShmemPmdMapped:        0 kB\n'
            'FilePmdMapped:         0 kB\n'
            'Shared_Hugetlb:        0 kB\n'
            'Private_Hugetlb:       0 kB\n'
            'Swap:                  0 kB\n'
            'SwapPss:               0 kB\n'
            'Locked:                0 kB\n'
            'THPeligible:    0\n'
            'ProtectionKey:         0\n'
            'VmFlags: mr mw me sd \n'
            'VmFlags: ex')

    def setUp(self):
        self.filename = 'assignment2.py'
        self.pypath = sys.executable
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
        try:
            self.a2 = import_module(self.filename.split('.')[0])
        except ModuleNotFoundError:
            print("Cannot find a function inside your assignment2.py. Do not rename or delete any of the required functions.")
    
    def test_rss_total(self):
        error = ('ERROR: not opening smaps for memory usage. Use open()'
                 ' and the arguments "/proc/<pid>/smaps". ')
        m = mock_open(read_data=self.data)
        with patch('builtins.open', m, create=True):
            given = self.a2.rss_mem_of_pid('whatever')
            expected = int(self.mem)
            self.assertEqual(given, expected, error)
            self.assertEqual(m.call_count, 1, error)


if __name__ == "__main__":
    unittest.main(buffer=True)
