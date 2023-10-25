# correction for gradient cycling

GE Premier, UHP, and 7T use diffusion gradient cycling (DGC) for thermal management.
The reduction in required cooling time allows for a shorter TR.
However, motion correction, even employing slice-to-volume registration, is suboptimal since the slices within one volume is not acquired subsequently.

This script converts the data between one-volume-one-encoding and one-volume-one-TR paradigms.
The one-volume-one-TR paradigm, whose slices within one volume are acquired in the same TR(s), are compatible with typical processing pipelines.
Therefore, the data acquired with diffusion gradient cycling can be conveniently motion-corrected by this conversion.

## prerequisite
- [nibabel](https://nipy.org/nibabel/)
- [numpy](https://numpy.org/)
- [python-fire](https://github.com/google/python-fire)

## usage

before motion correction:
`python ge_gradient_cycling_reorder.py data_with_dgc.nii.gz bvals tr_vols.nii.gz`

after motion correction:
`python ge_gradient_cycling_reorder.py tr_vols_corrected.nii.gz bvals encoding_vols_corrected.nii.gz --reverse`
