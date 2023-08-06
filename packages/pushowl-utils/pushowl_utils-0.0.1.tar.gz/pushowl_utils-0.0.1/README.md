# Build
python setup.py sdist

# Upload to PyPi
twine upload --config-file .pypirc --repository local dist/*

# PyPi configuration
```
[distutils]
index-servers =
  pypi
  local

[pypi]
repository=https://pypi.python.org/pypi

[local]
repository: https://pypi.pushowl.com
username: pushowl
password: <PASSWORD>
```