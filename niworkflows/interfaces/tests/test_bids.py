import numpy as np
import nibabel as nb
import pytest
from nipype.interfaces.base import Undefined


from .. import bids as bintfs


XFORM_CODES = {
    'MNI152Lin': 4,
    'T1w': 2,
    'boldref': 2,
    None: 1,
}

BOLD_PATH = 'ds054/sub-100185/func/sub-100185_task-machinegame_run-01_bold.nii.gz'


@pytest.mark.parametrize('space, size, units, xcodes, fixed', [
    ('T1w', (30, 30, 30, 10), ('mm', 'sec'), (2, 2), [False]),
    ('T1w', (30, 30, 30, 10), ('mm', 'sec'), (0, 2), [True]),
    ('T1w', (30, 30, 30, 10), ('mm', 'sec'), (0, 0), [True]),
    ('T1w', (30, 30, 30, 10), ('mm', None), (2, 2), [True]),
    ('T1w', (30, 30, 30, 10), (None, None), (0, 2), [True]),
    ('T1w', (30, 30, 30, 10), (None, 'sec'), (0, 0), [True]),
    ('MNI152Lin', (30, 30, 30, 10), ('mm', 'sec'), (4, 4), [False]),
    ('MNI152Lin', (30, 30, 30, 10), ('mm', 'sec'), (0, 2), [True]),
    ('MNI152Lin', (30, 30, 30, 10), ('mm', 'sec'), (0, 0), [True]),
    ('MNI152Lin', (30, 30, 30, 10), ('mm', None), (4, 4), [True]),
    ('MNI152Lin', (30, 30, 30, 10), (None, None), (0, 2), [True]),
    ('MNI152Lin', (30, 30, 30, 10), (None, 'sec'), (0, 0), [True]),
    (None, (30, 30, 30, 10), ('mm', 'sec'), (1, 1), [False]),
    (None, (30, 30, 30, 10), ('mm', 'sec'), (0, 0), [True]),
    (None, (30, 30, 30, 10), ('mm', 'sec'), (0, 2), [True]),
    (None, (30, 30, 30, 10), ('mm', None), (1, 1), [True]),
    (None, (30, 30, 30, 10), (None, None), (0, 2), [True]),
    (None, (30, 30, 30, 10), (None, 'sec'), (0, 0), [True]),
])
def test_DerivativesDataSink_bold(tmpdir, space, size, units, xcodes, fixed):
    tmpdir.chdir()

    hdr = nb.Nifti1Header()
    hdr.set_qform(np.eye(4), code=xcodes[0])
    hdr.set_sform(np.eye(4), code=xcodes[1])
    hdr.set_xyzt_units(*units)
    nb.Nifti1Image(np.zeros(size), np.eye(4), hdr).to_filename(
        'source.nii.gz')

    # BOLD derivative in T1w space
    dds = bintfs.DerivativesDataSink(
        base_directory=str(tmpdir),
        keep_dtype=True,
        desc='preproc',
        source_file=BOLD_PATH,
        space=space or Undefined,
        in_file='source.nii.gz'
    ).run()

    nii = nb.load(dds.outputs.out_file)
    assert dds.outputs.fixed_hdr == fixed
    assert int(nii.header['qform_code']) == XFORM_CODES[space]
    assert int(nii.header['sform_code']) == XFORM_CODES[space]
    assert nii.header.get_xyzt_units() == ('mm', 'sec')


T1W_PATH = 'ds054/sub-100185/anat/sub-100185_T1w.nii.gz'


@pytest.mark.parametrize('space, size, units, xcodes, fixed', [
    ('MNI152Lin', (30, 30, 30), ('mm', None), (4, 4), [False]),
    ('MNI152Lin', (30, 30, 30), ('mm', 'sec'), (4, 4), [True]),
    ('MNI152Lin', (30, 30, 30), ('mm', 'sec'), (0, 2), [True]),
    ('MNI152Lin', (30, 30, 30), ('mm', 'sec'), (0, 0), [True]),
    ('MNI152Lin', (30, 30, 30), (None, None), (0, 2), [True]),
    ('MNI152Lin', (30, 30, 30), (None, 'sec'), (0, 0), [True]),
    ('boldref', (30, 30, 30), ('mm', None), (2, 2), [False]),
    ('boldref', (30, 30, 30), ('mm', 'sec'), (2, 2), [True]),
    ('boldref', (30, 30, 30), ('mm', 'sec'), (0, 2), [True]),
    ('boldref', (30, 30, 30), ('mm', 'sec'), (0, 0), [True]),
    ('boldref', (30, 30, 30), (None, None), (0, 2), [True]),
    ('boldref', (30, 30, 30), (None, 'sec'), (0, 0), [True]),
    (None, (30, 30, 30), ('mm', None), (1, 1), [False]),
    (None, (30, 30, 30), ('mm', 'sec'), (1, 1), [True]),
    (None, (30, 30, 30), ('mm', 'sec'), (0, 2), [True]),
    (None, (30, 30, 30), ('mm', 'sec'), (0, 0), [True]),
    (None, (30, 30, 30), (None, None), (0, 2), [True]),
    (None, (30, 30, 30), (None, 'sec'), (0, 0), [True]),
])
def test_DerivativesDataSink_t1w(tmpdir, space, size, units, xcodes, fixed):
    tmpdir.chdir()

    hdr = nb.Nifti1Header()
    hdr.set_qform(np.eye(4), code=xcodes[0])
    hdr.set_sform(np.eye(4), code=xcodes[1])
    hdr.set_xyzt_units(*units)
    nb.Nifti1Image(np.zeros(size), np.eye(4), hdr).to_filename(
        'source.nii.gz')

    # BOLD derivative in T1w space
    dds = bintfs.DerivativesDataSink(
        base_directory=str(tmpdir),
        keep_dtype=True,
        desc='preproc',
        source_file=T1W_PATH,
        space=space or Undefined,
        in_file='source.nii.gz'
    ).run()

    nii = nb.load(dds.outputs.out_file)
    assert dds.outputs.fixed_hdr == fixed
    assert int(nii.header['qform_code']) == XFORM_CODES[space]
    assert int(nii.header['sform_code']) == XFORM_CODES[space]
    assert nii.header.get_xyzt_units() == ('mm', 'unknown')


@pytest.mark.parametrize('field', [
    'RepetitionTime',
    'UndefinedField',
])
def test_ReadSidecarJSON_connection(testdata_dir, field):
    """
    This test prevents regressions of #333
    """
    from nipype.pipeline import engine as pe
    from nipype.interfaces import utility as niu
    from niworkflows.interfaces.bids import ReadSidecarJSON

    reg_fields = ['RepetitionTime']
    n = pe.Node(ReadSidecarJSON(fields=reg_fields), name='node')
    n.inputs.in_file = str(testdata_dir / 'ds054' / 'sub-100185' / 'fmap' /
                           'sub-100185_phasediff.nii.gz')
    o = pe.Node(niu.IdentityInterface(fields=['out_port']), name='o')
    wf = pe.Workflow(name='json')

    if field in reg_fields:  # This should work
        wf.connect([
            (n, o, [(field, 'out_port')]),
        ])
    else:
        with pytest.raises(Exception, match=r'.*Some connections were not found.*'):
            wf.connect([
                (n, o, [(field, 'out_port')]),
            ])
