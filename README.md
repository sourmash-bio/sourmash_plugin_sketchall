# sourmash_plugin_sketchall

Sketch many files at once.

This is a sourmash plugin.

Usage:
```shell
sourmash scripts sketchall <directory> -j 8
```

This will use 8 processes to (attempt to) sketch all of the files
underneath `directory`.  Filenames ending in `.sig` or `.sig.gz` will
be ignored.
