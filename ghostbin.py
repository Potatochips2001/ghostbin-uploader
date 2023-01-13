#!/usr/bin/env python3
import requests
import os
import argparse
import pyperclip

parser = argparse.ArgumentParser(
    description="Upload a file to ghostbin.me with this script."
)

parser.add_argument("--copy", action='store_true', help="Copy link after uploading")
parser.add_argument("--debug", action='store_true', help="Show overview info")
parser.add_argument("--file", help="File to upload")
parser.add_argument("--title", help="Title for paste")

args = parser.parse_args()

def get_syntax(ext):
    global syntax_list
    for i in syntax_list:
        if (ext == i):
            return syntax_list[i]
    return "plain"

syntax_list ={
    ".py": "x-python",
    ".html": "html",
    ".js": "javascript",
    ".css": "css",
    ".xml": "xml",
    ".cs": "x-csharp",
    ".sh": "x-sh",
    ".sql": "x-sql",
    ".php": "x-php",
    ".java": "x-java",
    ".cpp": "x-c++src"
}

content = ""
title = ""
syntax = "plain"

payload = {
    "content": content,
    "title": title,
    "syntax": syntax
}


if (args.title != None):
    title = args.title
else:
    title = input("Title: ")

if (args.file != None):
    file_location = args.file
else:
    file_location = input("Location to file: ")


f = open(file_location, 'r')
content = f.read()
f.close()

file_ext = os.path.splitext(file_location)[1]

payload['title'] = title
payload['content'] = content
payload['syntax'] = get_syntax(file_ext)

if (args.debug):
    print(f'''
Data overview:
title: {payload["title"]}
content: {payload["content"]}
syntax: {payload["syntax"]}
    ''')

req = requests.post("https://ghostbin.me/create.php", data=payload)

uri = req.url

if (args.copy):
    pyperclip.copy(uri)
    print(f"Your paste: {uri} - Copied!")
else:
    print(f"Your paste: {req.url}")
