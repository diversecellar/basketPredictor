# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 12:53:28 2025

@author: Paul Namalomba
"""

from datetime import datetime as dt
from datetime import timedelta as td
import os
import sys
from docx import Document
import glob as gb
import dt_prompter

date_prompt = dt_prompter.date_prompt2
date_now = dt.now() - td(days = date_prompt)
sngl_ws = " " # single whitespace
os_sep = str(os.sep)
dbl_ws = "  " # single whitespace
date_today = date_now
month_today = date_today.strftime("%b")
day_today = date_today.strftime("%d")
year_today = date_today.strftime("%Y")
text_to_replace = day_today+sngl_ws+month_today+sngl_ws+year_today
#print(text_to_replace)
betweek_name = date_today.strftime("%y")+date_today.strftime("%m")+date_today.strftime("%d")
sport_hook = "-bball"
docx_file_ext = ".docx"
docx_file_name = betweek_name+sport_hook+docx_file_ext
pdf_file_ext = ".pdf"
pdf_file_name = betweek_name+sport_hook+pdf_file_ext
code_dir = os.getcwd()
betweek_dir = os.path.join(code_dir+os_sep+betweek_name)
#print("--------------------------------")
if os.path.exists(betweek_dir):
    os.chdir(betweek_dir)
    betweek_subfiles = gb.glob("*.docx", recursive=False)
    if docx_file_name in betweek_subfiles:
        docx_file_path = os.path.join(betweek_dir+os_sep+docx_file_name)
        docx_doc = Document(docx_file_name)
        line_count = 0
        for line in docx_doc.paragraphs:
            line_count += 1
            if text_to_replace not in line.text and line_count == 1:
                line.text = line.text.replace(line.text[-11:], text_to_replace)
                line_runs = line.runs
                for i in range(len(line_runs)):
                    line_runs[i].font.bold = True
                    line_runs[i].font.underline = True
            else:
                line_runs = line.runs
                for i in range(len(line_runs)):
                    line_runs[i].font.bold = True
                    line_runs[i].font.underline = True
        docx_doc.save(docx_file_name)
        exec(open('docx-file-opener.py').read())
    betweek_pdfs = gb.glob("*.pdf", recursive=False)
    if len(betweek_pdfs) > 0:
        pdf_file_path = os.path.join(betweek_dir+os_sep+pdf_file_name)
        if os.path.isfile(pdf_file_path) or os.path.islink(pdf_file_path):
            try:
                os.unlink(pdf_file_path)
                os.remove(pdf_file_path)
            except Exception as e:
                whatever = e
os.chdir(code_dir)