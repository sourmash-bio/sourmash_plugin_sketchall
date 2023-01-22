import os
from sourmash.logging import debug_literal, set_quiet

print(config['debug'])
debug = bool(int(config['debug']))
set_quiet(False, debug)

DIRNAME = config['location']
debug_literal(f"sketchall: running on '{DIRNAME}'")

# find all files that don't end in .sig.gz or .sig, run on 'em
FILES = []
for root, dirs, files in os.walk(DIRNAME, topdown=False):
    for name in files:
        if not name.endswith('.sig') and not name.endswith('.sig.gz'):
            filename = os.path.join(root, name)
            FILES.append(filename + '.sig.gz')

debug_literal(f"found {len(FILES)} files.")

rule all:
    input:
        FILES

rule sketch_wc:
    input: "{genome}"
    output: "{genome}.sig.gz"
    threads: 1
    shell: """
       sourmash sketch dna {input} -o {output}
    """
