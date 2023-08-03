#! /usr/bin/env python
"""\
sketch many genomes efficiently using multiple threads.

By default, 'sketchall' ignores files ending in '.sig', '.sig.gz',
'.zip', '.sqldb', and attempts to sketch all other files.
"""

usage="""
   sourmash scripts sketchall <directory>
"""

epilog="""
See https://github.com/sourmash-bio/sourmash_plugin_sketchall for examples.

Need help? Have questions? Ask at http://github.com/sourmash/issues!
"""

#IDEAS:
#- support taking in a CSV or file list instead?
#- support ignoring or limiting to a particular extension

import os
import sys
import argparse
import pathlib
from concurrent.futures import ThreadPoolExecutor

import screed
import sourmash
from sourmash import plugins
from sourmash.logging import debug_literal, notify, error
from sourmash.command_sketch import _signatures_for_sketch_factory
from sourmash.command_compute import add_seq, set_sig_name
from sourmash import sourmash_args


class Command_SketchAll(plugins.CommandLinePlugin):
    command = 'sketchall'
    description = ""

    description = __doc__
    usage = usage
    epilog = epilog
    formatter_class = argparse.RawTextHelpFormatter

    def __init__(self, p):
        super().__init__(p)
        p.add_argument('directory',
                       help="directory to @CTB xyz")
        p.add_argument('-j', '-c', '--cores', type=int, default=4,
                       help="number of processes/cores to use")
        p.add_argument('--extension', default='zip',
                       choices={ "sig", "sig.gz", "zip", "sqldb" })
        p.add_argument('-p', '--param-string', default=['dna'],
                       help='signature parameters to use.', action='append')
        p.add_argument('-o', '--outdir', '--output-directory',
                       help="where to put calculated signatures @CTB xzy")

    def main(self, args):
        super().main(args)
        debug_literal(f"sketchall main: location is {args.directory}")

        debug = 1 if args.debug else 0

        # build params obj & sketching factories
        factories = []
        for p in args.param_string:
            f = _signatures_for_sketch_factory(args.param_string, 'dna')
            factories.append(f)

        # find all files that are not sketches, run 'em
        FILES = []
        ignore_exts = { '.sig', '.sig.gz', '.zip', '.sqldb' }

        toplevel = args.directory
        for filepath in pathlib.Path(toplevel).rglob('*'):
            if filepath.is_file():
                relpath = filepath.relative_to(toplevel)
                relpath = relpath.as_posix()

                keep = True
                for ext in ignore_exts:
                    if relpath.endswith(ext):
                        keep = False
                        break

                if keep:
                    FILES.append((toplevel, relpath))

        debug_literal(f"found {len(FILES)} files.")

        # @CTB break out/error out if nothing there
        # @CTB check if it's a directory?

        outdir = args.outdir
        if outdir and not os.path.isdir(args.outdir):
            try:
                debug_literal(f"trying to make {outdir}")
                os.mkdir(outdir)
            except:
                error(f"Cannot make output directory '{outdir}'; exiting.")
                sys.exit(-1)

        notify(f"Starting to sketch {len(FILES)} files with {args.cores} threads.")
        # run things in parallel:
        if args.cores > 1:
            with ThreadPoolExecutor(max_workers=args.cores) as executor:
                for (toplevel, relpath) in FILES:
                    executor.submit(compute_sig, factories, toplevel, relpath,
                                    extension=args.extension,
                                    outdir=outdir)
        else:
            notify(f"NOTE: running in serial mode, not parallel, because cores={args.cores}")
            for (toplevel, relpath) in FILES:
                compute_sig(factories, toplevel, relpath,
                            extension=args.extension, outdir=outdir)


def compute_sig(factories, toplevel, relpath, *, extension='zip', outdir=None):
    "Build one set of sketches for the given filename."
    sigfile = relpath + '.' + extension
    if outdir:
        sigfile = os.path.join(outdir, sigfile)
    else:
        sigfile = os.path.join(toplevel, sigfile)

    filename = os.path.join(toplevel, relpath)
    debug_literal(f"processing '{filename}' => '{sigfile}'")

    name = None
    try:
        with screed.open(filename) as screed_iter:
            if not screed_iter:
                notify(f"no sequences found in '{filename}'; skipping.")
                return

            sigslist = [ f() for f in factories ]

            for n, record in enumerate(screed_iter):
                if n % 10000 == 0:
                    if n:
                        notify('\r...{} {}', filename, n, end='')

                try:
                    for sigs in sigslist:
                        add_seq(sigs, record.sequence, False, False)

                    name = record.name
                except ValueError as exc:
                    error(f"ERROR when reading from '{filename}' - ")
                    error(str(exc))
                    return

                notify('...{} {} sequences', filename, n, end='')

    except ValueError:
        return

    with sourmash_args.SaveSignaturesToLocation(sigfile) as save_sig:
        for sigs in sigslist:
            set_sig_name(sigs, filename, name)
            for ss in sigs:
                save_sig.add(ss)

    debug_literal(f'saved {len(save_sig)} sketch(es) for {filename} to {sigfile}')
