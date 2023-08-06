#!/usr/bin/python

import pkg_resources
import os
import sys

readme_html_path = pkg_resources.resource_filename(__name__, 'README.html')
print(readme_html_path)
readme_html_path = os.path.join(sys.prefix, 'README.html')
print(readme_html_path)
with open(readme_html_path) as f:
    print(f.read())
