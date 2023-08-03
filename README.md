# sourmash_plugin_sketchall

Sketch many files at once with sourmash, using threads.

The `sketchall` plugin is a convenient way to:
* automatically discover & sketch many sequence files in a directory hierarchy.
* speed up sketching using multiple threads.

## Installation

```
pip install sourmash_plugin_sketchall
```

This will use 8 processes to (attempt to) sketch all of the files
underneath `directory`.  Filenames ending in `.sig` or `.sig.gz` will
be ignored.

## Usage

The following command:
```shell
sourmash scripts sketchall examples -j 8
```
will use 8 threads to (attempt to) sketch all of the files
underneath `examples`.  Filenames ending in `.sig`, `.sig.gz`,
`.zip`, and `.sqldb` will
be ignored, and failed files will be reported (but failures will be
ignored).

By default, `sketchall` will save signatures in place: sketches for
`examples/10.fa.gz` are saved to `examples/10.fa.gz.zip`, and sketches
for `examples/subdir/2.fa.gz` are saved to
`examples/subdir/2.fa.gz.zip`.

With `-o/--output-directory`, `sketchall` will sketch into a new hierarchy
of files; so, for example,
```shell
sourmash scripts sketchall examples -o sigs/
```
will save the sketch for `examples/subdir/2.fa.gz` to `sigs/subdir/2.fa.gz`.

The default signature format for `sketchall` is `.zip`. This can be changed
by using `--extension`:
```shell
sourmash scripts sketchall examples -o sigs/ --extension .sig.gz
```
will create `sigs/10.fa.gz.sig.gz` and `sigs/subdir/2.fa.gz.sig.gz`.

The pattern for files to sketch can be set by using `--pattern`:
```shell
sourmash scripts sketchall examples --pattern "2.*.gz"
```

>>>>>>> ac9f1e204dfda7ef99c9dd70307023f6e94c0c24
The parameter string used to sketch files can be changed with `-p/--param-string`:
```
sourmash scripts sketchall examples -p k=21 examples/ -o output.k21
```

After `sketchall`, `sourmash sig cat` can be used to collect all of the
sketches into a single zip file, e.g.
```shell
sourmash sig cat sigs -o all-sigs.zip
```

## Benchmarks and speedups

On a small collection of 64 genomes, using 4-8 threads more than
doubles the speed of sketching - for larger files, speedups should
approach linear scaling.

Wall time (s) | Threads | Efficiency
-- | -- | --
6.00 | 1 | 106%
2.84 | 4 | 306%
2.41 | 8 | 321%

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
