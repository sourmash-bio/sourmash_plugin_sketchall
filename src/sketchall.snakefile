print('XXX', config['dir'])

genomes, = glob_wildcards(f"{config['dir']}/{{g}}")

# remove .sig files
genomes = [ g for g in genomes if not g.endswith('.sig') ]

rule all:
    input:
        expand(f"{config['dir']}/{{g}}.sig", g=genomes)

rule sketch_wc:
    input: "{genome}"
    output: "{genome}.sig"
    threads: 1
    shell: """
       sourmash sketch dna {input} -o {output}
    """
