"""
Tests for sourmash_plugin_xyz.
"""
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


def test_on_all_outdir(runtmp, cores):
    all_data = utils.get_test_data('')
    outdir = runtmp.output('')

    runtmp.sourmash('scripts', 'sketchall', all_data,
                    '-o', outdir, '-j', cores)

    print(runtmp.last_result.out)
    print(runtmp.last_result.err)
    assert runtmp.last_result.status == 0

    # check main dir output
    ex_output = runtmp.output('10.fa.gz.zip')
    assert os.path.exists(ex_output)

    # check subdir output
    ex_output = runtmp.output('subdir/1.fa.gz.zip')
    assert os.path.exists(ex_output)


def test_on_all_inplace(runtmp, cores):
    all_data = utils.get_test_data('')
    outdir = runtmp.output('inplace')

    shutil.copytree(all_data, outdir)

    runtmp.sourmash('scripts', 'sketchall', outdir, '-j', cores)

    print(runtmp.last_result.out)
    print(runtmp.last_result.err)
    assert runtmp.last_result.status == 0

    # check main dir output
    ex_output = runtmp.output('inplace/10.fa.gz.zip')
    assert os.path.exists(ex_output)

    # check subdir output
    ex_output = runtmp.output('inplace/subdir/1.fa.gz.zip')
    assert os.path.exists(ex_output)
