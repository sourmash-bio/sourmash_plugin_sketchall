# sourmash_plugin_sketchall

Sketch many files at once with sourmash, using threads.

## Installation

```
pip install sourmash_plugin_sketchall
```

## Usage

The following command:
```shell
sourmash scripts sketchall examples -j 8
```
will use 8 threads to (attempt to) sketch all of the files
underneath `examples`.  Filenames ending in `.sig` or `.sig.gz` will
be ignored, and failed files will be reported (but failures will be
ignored).

By default, `sketchall` will save signatures in place: sketches for
`examples/10.fa.gz` are saved to `examples/10.fa.gz.zip`, and sketches
for `examples/subdir/2.fa.gz` are saved to
`examples/subdir/2.fa.gz.zip`.

With `-o/--output-directory`, `sketchall` will create a new hierarchy
of directories; so, for example,
```shell
sourmash scripts sketchall examples -o sigs/
```
will save the sketch for `examples/subdir/1.fa.gz` to `sigs/subdir/1.fa.gz`.

The default signature format for `sketchall` is `.zip`. This can be changed
by using `--extension`:
```shell
sourmash scripts sketchall examples -o sigs/ --extension .sig.gz
```
will create `sigs/10.fa.gz.sig.gz` and `sigs/subdir/1.fa.gz.sig.gz`.

After `sketchall`, `sourmash sig cat` can be used to collect all of the
sketches into a single zip file, e.g.
```shell
sourmash sig cat sigs -o all-sigs.zip
```

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
