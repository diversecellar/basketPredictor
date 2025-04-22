#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 11:17:40 2025

@author: kb
"""
import argparse
import os

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-b','--betday', type=str, help='how many days is next betday (int)')
parser.add_argument('-r','--run', type=int, help='logic for whether to run script or see past files (only 1 or 0) passable')
parser.add_argument('-l','--level', type=int, help='if failed, tell level of fail and start from there', nargs='?', const=0)
args = parser.parse_args()

default2 = os.getcwd()
exec(open('args_parser.py').read())
os.chdir(default2)
exec(open('main.py').read())
os.chdir(default2)