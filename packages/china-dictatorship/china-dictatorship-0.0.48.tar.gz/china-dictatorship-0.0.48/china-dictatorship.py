#!/usr/bin/python3

try:
  import importlib.resources as importlib_resources
except ImportError:
  # In PY<3.7 fall-back to backported `importlib_resources`.
  import importlib_resources

readme_html_path = importlib_resources.read_text('china_dictatorship', 'README.html')
with open(readme_html_path) as f:
    print(f.read())
