#!/usr/bin/env python3

import re
import sys

import requests

if not len(sys.argv) == 2:
    exit(
        f'error: invalid arguments\nusage: python {sys.argv[0]} http://example.com')

url = sys.argv[1]

if not re.search(r'^(http|https)://', url):
    exit(f'error: invalid url.')

response = requests.get(url, headers={
    'user-agent': 'thankunext/1.0'
})

if not (build_manifest_path := re.search(r'/_next/static/[\w-]+/_buildManifest\.js', response.text)):
    exit('error: _buildManifest.js was not found. is this site really running Next.js?')

build_manifest_path = build_manifest_path.group()
build_manifest_response = requests.get(url + build_manifest_path, headers={
    'user-agent': 'thankunext/1.0'
})

paths = re.findall(
    r'(?<=\")[a-zA-Z0-9_/\[\]\.]+(?=\")', build_manifest_response.text)

paths = sorted(set(paths))

print('\n'.join(paths))
