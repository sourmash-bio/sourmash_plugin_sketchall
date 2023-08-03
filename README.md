# sourmash_plugin_sketchall

Sketch many files at once.

This is a sourmash plugin.

Usage:
```shell
sourmash scripts sketchall <directory> -j 8
```

<<<<<<< Updated upstream
This will use 8 processes to (attempt to) sketch all of the files
underneath `directory`.  Filenames ending in `.sig` or `.sig.gz` will
be ignored.
=======
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
>>>>>>> Stashed changes
