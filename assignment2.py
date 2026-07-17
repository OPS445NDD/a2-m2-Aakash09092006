#!/usr/bin/env python3

'''
OPS445 Assignment 2 - Summer 2026
Program: ana56 
Author: "Student Name"
The python code in this file is original work written by
"Student Name". No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: A memory visualizer tool that parses system and process 
             memory data from /proc and displays it using bar charts.

Date: July 2026
'''

import argparse
import os
import sys

def parse_command_args() -> object:
    "Set up argparse here. Call this function inside main."
    parser = argparse.ArgumentParser(
        description="Memory Visualiser -- See Memory Usage Report with bar charts",
        epilog="Copyright 2023"
    )
    parser.add_argument(
        "-l", "--length", 
        type=int, 
        default=20, 
        help="Specify the length of the graph. Default is 20."
    )
    parser.add_argument(
        "-H", "--human-readable", 
        action="store_true", 
        help="Prints sizes in human readable format"
    )
    parser.add_argument(
        "program", 
        type=str, 
        nargs='?', 
        help="if a program is specified, show memory use of all associated processes. Show only total use if not."
    )
    args = parser.parse_args()
    return args

def percent_to_graph(percent: float, length: int=20) -> str:
    "turns a percent 0.0 - 1.0 into a bar graph"
    num_hashes = int(round(percent * length))
    num_spaces = length - num_hashes
    return f"[{'#' * num_hashes}{' ' * num_spaces}]"

def get_sys_mem() -> int:
    "return total system memory (used or available) in kB"
    with open("/proc/meminfo", "r") as f:
        for line in f:
            if line.startswith("MemTotal:"):
                return int(line.split()[1])
    return 0

def get_avail_mem() -> int:
    "return total memory that is currently available"
    mem_free = 0
    swap_free = 0
    with open("/proc/meminfo", "r") as f:
        for line in f:
            if line.startswith("MemAvailable:"):
                return int(line.split()[1])
            elif line.startswith("MemFree:"):
                mem_free = int(line.split()[1])
            elif line.startswith("SwapFree:"):
                swap_free = int(line.split()[1])
    return mem_free + swap_free

def pids_of_prog(app_name: str) -> list:
    "given an app name, return all pids associated with app"
    output = os.popen('pidof ' + app_name).read().strip()
    if output == '':
        return []
    return output.split()

def rss_mem_of_pid(proc_id: str) -> int:
    "given a process id, return the Resident memory used"
    total_rss = 0
    try:
        with open('/proc/' + str(proc_id) + '/smaps', 'r') as f:
            for line in f:
                if line.startswith("Rss:"):
                    total_rss += int(line.split()[1])
    except (FileNotFoundError, PermissionError):
        return 0
    return total_rss

def bytes_to_human_r(kibibytes: int, decimal_places: int=2) -> str:
    "turn 1,024 into 1 MiB, for example"
    suffixes = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB']
    suf_count = 0
    result = kibibytes 
    while result > 1024 and suf_count < len(suffixes) - 1:
        result /= 1024
        suf_count += 1
    return f"{result:.{decimal_places}f} {suffixes[suf_count]}"

if __name__ == "__main__":
    args = parse_command_args()
    
    total_mem = get_sys_mem()
    avail_mem = get_avail_mem()
    used_mem = total_mem - avail_mem
    sys_percent = used_mem / total_mem if total_mem > 0 else 0.0

    if not args.program:  
        graph = percent_to_graph(sys_percent, args.length)
        percent_label = f"{int(round(sys_percent * 100))}%"
        
        if args.human_readable:
            total_str = bytes_to_human_r(total_mem)
            used_str = bytes_to_human_r(used_mem)
            print(f"Memory         {graph[:-1]} | {percent_label}] {used_str}/{total_str}")
        else:
            print(f"Memory         {graph[:-1]} | {percent_label}] {used_mem}/{total_mem}")
            
    else:
        pids = pids_of_prog(args.program)
        
        if not pids:
            print(f"{args.program} not found")
            sys.exit(0)
            
        total_pid_rss = 0
        
        for pid in pids:
            pid_rss = rss_mem_of_pid(pid)
            total_pid_rss += pid_rss
            
            pid_percent = pid_rss / total_mem if total_mem > 0 else 0.0
            pid_graph = percent_to_graph(pid_percent, args.length)
            pid_percent_label = f"{int(round(pid_percent * 100))}%"
            
            if args.human_readable:
                pid_rss_str = bytes_to_human_r(pid_rss)
                total_str = bytes_to_human_r(total_mem)
                print(f"{pid:<14} {pid_graph[:-1]} | {pid_percent_label}] {pid_rss_str}/{total_str}")
            else:
                print(f"{pid:<14} {pid_graph[:-1]} | {pid_percent_label}] {pid_rss}/{total_mem}")
                
        prog_percent = total_pid_rss / total_mem if total_mem > 0 else 0.0
        prog_graph = percent_to_graph(prog_percent, args.length)
        prog_percent_label = f"{int(round(prog_percent * 100))}%"
        
        if args.human_readable:
            total_pid_rss_str = bytes_to_human_r(total_pid_rss)
            total_str = bytes_to_human_r(total_mem)
            print(f"{args.program:<14} {prog_graph[:-1]} | {prog_percent_label}] {total_pid_rss_str}/{total_str}")
        else:
            print(f"{args.program:<14} {prog_graph[:-1]} | {prog_percent_label}] {total_pid_rss}/{total_mem}")
