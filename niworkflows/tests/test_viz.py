# -*- coding: utf-8 -*-
"""Test viz module"""
import os
import nibabel as nb
from .. import viz
from .conftest import datadir


def test_carpetplot():
    """Write a carpetplot"""
    out_file = None
    save_artifacts = os.getenv('SAVE_CIRCLE_ARTIFACTS', False)
    if save_artifacts:
        out_file = os.path.join(save_artifacts, 'carpetplot.svg')
    viz.plot_carpet(
        os.path.join(datadir, 'sub-ds205s03_task-functionallocalizer_run-01_bold_volreg.nii.gz'),
        nb.load(os.path.join(
            datadir,
            'sub-ds205s03_task-functionallocalizer_run-01_bold_parc.nii.gz')).get_data(),
        output_file=out_file,
        legend=True
    )


def test_plot_melodic_components():
    """Test plotting melodic components"""
    import numpy as np
    # save the artifacts
    save_artifacts = os.getenv('SAVE_CIRCLE_ARTIFACTS', False)
    all_noise = 'melodic_all_noise.svg'
    no_noise = 'melodic_no_noise.svg'
    no_classified = 'melodic_no_classified.svg'

    if save_artifacts:
        all_noise = os.path.join(save_artifacts, 'melodic_all_noise.svg')
        no_noise = os.path.join(save_artifacts, 'melodic_no_noise.svg')
        no_classified = os.path.join(save_artifacts, 'melodic_no_classified.svg')

    # melodic directory
    os.makedirs('melodic', exist_ok=True)
    melodic_dir = os.path.join(os.getcwd(), "melodic")
    # melodic_mix
    mel_mix = np.random.randint(low=-5, high=5, size=[10, 2])
    mel_mix_file = os.path.join(melodic_dir, "melodic_mix")
    np.savetxt(mel_mix_file, mel_mix, fmt='%i')
    # melodic_FTmix
    mel_ftmix = np.random.rand(2, 5)
    mel_ftmix_file = os.path.join(melodic_dir, "melodic_FTmix")
    np.savetxt(mel_ftmix_file, mel_ftmix)
    # melodic_ICstats
    mel_icstats = np.random.rand(2, 2)
    mel_icstats_file = os.path.join(melodic_dir, "melodic_ICstats")
    np.savetxt(mel_icstats_file, mel_icstats)
    # melodic_IC
    mel_ic = np.random.rand(2, 2, 2, 2)
    mel_ic_file = os.path.join(melodic_dir, "melodic_IC.nii.gz")
    mel_ic_img = nb.Nifti2Image(mel_ic, np.eye(4))
    mel_ic_img.to_filename(mel_ic_file)
    # noise_components
    noise_comps = np.array([1, 2])
    noise_comps_file = os.path.join(os.getcwd(), 'noise_ics.csv')
    np.savetxt(noise_comps_file, noise_comps,
               fmt='%i', delimiter=',')

    # create empty components file
    nocomps_file = os.path.join(os.getcwd(), 'noise_none.csv')
    open(nocomps_file, 'w').close()

    # in_file
    voxel_ts = np.random.rand(2, 2, 2, 10)
    in_file = nb.Nifti2Image(voxel_ts, np.eye(4))
    in_file.to_filename('in_file.nii.gz')
    # report_mask
    report_mask = nb.Nifti2Image(np.ones([2, 2, 2]), np.eye(4))
    report_mask.to_filename('report_mask.nii.gz')

    # run command with all noise components
    viz.utils.plot_melodic_components(melodic_dir, 'in_file.nii.gz', tr=2.0,
                                      report_mask='report_mask.nii.gz',
                                      noise_components_file=noise_comps_file,
                                      out_file=all_noise)
    # run command with no noise components
    viz.utils.plot_melodic_components(melodic_dir, 'in_file.nii.gz', tr=2.0,
                                      report_mask='report_mask.nii.gz',
                                      noise_components_file=nocomps_file,
                                      out_file=no_noise)

    # run command without noise components file
    viz.utils.plot_melodic_components(melodic_dir, 'in_file.nii.gz', tr=2.0,
                                      report_mask='report_mask.nii.gz',
                                      out_file=no_classified)
