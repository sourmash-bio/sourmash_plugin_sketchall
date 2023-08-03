"""
Tests for sourmash_plugin_xyz.
"""

# CTB: test
# - pattern
# - -p param string
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

    # check subdir output
    ex_output = runtmp.output(f'subdir/1.fa.gz.{use_extension}')
    assert os.path.exists(ex_output), ex_output


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
