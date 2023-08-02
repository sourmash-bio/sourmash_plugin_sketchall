# sourmash_plugin_sketchall

Sketch many files at once with sourmash, using threads.

## Installation

```
pip install sourmash_plugin_sketchall
```

## Usage

```shell
sourmash scripts sketchall <directory> -j 8
```

This will use 8 processes to (attempt to) sketch all of the files
underneath `directory`.  Filenames ending in `.sig` or `.sig.gz` will
be ignored.

## Support

We suggest filing issues in
[the main sourmash issue tracker](https://github.com/dib-lab/sourmash/issues)
as that receives more attention!

## Dev docs

`sketchall` is developed at https://github.com/sourmash-bio/sourmash_plugin_sketchall.

### Testing

Run:
```
pytest tests
```

### Generating a release

Bump version number in `pyproject.toml` and push.

Make a new release on github.

Then pull, and:

```
python -m build
```

followed by `twine upload dist/...`.
