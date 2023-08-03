"""
Tests for sourmash_plugin_xyz.
"""

# CTB: test TODO:
# - pattern
# sig cat advice

import os
import pytest
import shutil

import sourmash
import sourmash_tst_utils as utils
from sourmash_tst_utils import SourmashCommandFailed


def test_run_sourmash(runtmp):
    with pytest.raises(SourmashCommandFailed):
        runtmp.sourmash('', fail_ok=True)

    print(runtmp.last_result.out)
    print(runtmp.last_result.err)
    assert runtmp.last_result.status != 0                    # no args provided, ok ;)


def test_on_all_outdir(runtmp, cores, use_extension):
    all_data = utils.get_test_data('')
    outdir = runtmp.output('')

    runtmp.sourmash('scripts', 'sketchall', all_data,
                    '-o', outdir, '-j', cores, '--extension', use_extension)

    print(runtmp.last_result.out)
    print(runtmp.last_result.err)
    assert runtmp.last_result.status == 0

    # check main dir output
    ex_output = runtmp.output(f'10.fa.gz.{use_extension}')
    assert os.path.exists(ex_output), ex_output
    sigs = list(sourmash.load_file_as_signatures(ex_output))
    assert len(sigs) == 1
    assert sigs[0].minhash.ksize == 31
    assert sigs[0].minhash.moltype == 'DNA'

    # check subdir output
    ex_output = runtmp.output(f'subdir/1.fa.gz.{use_extension}')
    assert os.path.exists(ex_output), ex_output
    sigs = list(sourmash.load_file_as_signatures(ex_output))
    assert len(sigs) == 1
    assert sigs[0].minhash.ksize == 31
    assert sigs[0].minhash.moltype == 'DNA'


def test_on_all_inplace(runtmp, cores, use_extension):
    all_data = utils.get_test_data('')
    outdir = runtmp.output('inplace')

    shutil.copytree(all_data, outdir)

    runtmp.sourmash('scripts', 'sketchall', outdir, '-j', cores,
                    '--extension', use_extension)

    print(runtmp.last_result.out)
    print(runtmp.last_result.err)
    assert runtmp.last_result.status == 0

    # check main dir output
    ex_output = runtmp.output(f'inplace/10.fa.gz.{use_extension}')
    assert os.path.exists(ex_output), ex_output

    # check subdir output
    ex_output = runtmp.output(f'inplace/subdir/1.fa.gz.{use_extension}')
    assert os.path.exists(ex_output), ex_output


def test_on_all_param(runtmp, cores):
    all_data = utils.get_test_data('')
    outdir = runtmp.output('')

    runtmp.sourmash('scripts', 'sketchall', all_data,
                    '-o', outdir, '-j', cores, '-p', 'k=51')

    print(runtmp.last_result.out)
    print(runtmp.last_result.err)
    assert runtmp.last_result.status == 0

    # check main dir output
    ex_output = runtmp.output(f'10.fa.gz.zip')
    assert os.path.exists(ex_output), ex_output
    sigs = list(sourmash.load_file_as_signatures(ex_output))
    assert len(sigs) == 1
    assert sigs[0].minhash.ksize == 51
    assert sigs[0].minhash.moltype == 'DNA'

    # check subdir output
    ex_output = runtmp.output(f'subdir/1.fa.gz.zip')
    assert os.path.exists(ex_output), ex_output
    sigs = list(sourmash.load_file_as_signatures(ex_output))
    assert len(sigs) == 1
    assert sigs[0].minhash.ksize == 51
    assert sigs[0].minhash.moltype == 'DNA'
