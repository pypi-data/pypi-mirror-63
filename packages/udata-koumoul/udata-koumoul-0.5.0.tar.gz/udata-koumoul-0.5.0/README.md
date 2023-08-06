# udata-koumoul

Theme for Koumoul's demo opendata portal

## Usage

Install the theme package in you udata environement:

```bash
pip install udata-koumoul
```

Then, define the installed theme as current in you `udata.cfg`:

```python
THEME = 'koumoul'
```

## Development

There is a `docker-compose` configuration to get started fast.
Just run:

```bash
docker-compose up
```

Then go to <http://localhost:7000> to connect to the development server
with live reload.

## Publish

```
python setup.py sdist bdist_wheel
twine upload dist/*
```
