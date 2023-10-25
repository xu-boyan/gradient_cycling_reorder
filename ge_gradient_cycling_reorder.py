#!/usr/bin/env python

import nibabel as nib
import numpy as np
import fire


def slice_acquisition_order(n_ex, is_descending=False):
    # interleaved
    z_locations = np.concatenate([np.arange(0,n_ex,2), np.arange(1, n_ex, 2)])
    if is_descending:
        for i in range(i, n_ex/2):
            z_locations[i], z_locations[n_ex-1-i] =  z_locations[n_ex-1-i], z_locations[i]
    return z_locations


def reorder(n_vol, n_ex, reverse=False):
    """
    rearrange the slice indices
    slices with same diffusion encoding to slices acquired in one TR
    """
    vol_ex_old = np.array([[i]*n_ex for i in range(n_vol)])
    vol_ex_new = np.zeros_like(vol_ex_old, dtype=int)
    z_locations = slice_acquisition_order(n_ex)
    shift_sign = 1 if reverse else -1
    for i in np.arange(0, n_ex):
        i_ex = z_locations[i]
        vol_ex_new[:, i_ex] = np.roll(vol_ex_old[:, i_ex], shift_sign*i)
    
    return vol_ex_new


def encoding_to_tr(nii_file, 
                   bval_file,
                   out_file,
                   reverse=False,
                   diffusion_optimization_window=1, 
                   hyperband=1):
    print("tr to encoding" if reverse else "encoding to tr")

    bvals = np.genfromtxt(bval_file, dtype=float)
    img = nib.load(nii_file)
    vol = img.get_fdata()

    if vol.shape[3] != len(bvals):
        raise ValueError("The NIfTI file and the bval file do not match.")

    if hyperband == 1:
        n_ex = vol.shape[2]
    else:
        raise NotImplementedError("Hyberband is not supported yet.")
    
    if diffusion_optimization_window == 1:
        dwi_idx = np.nonzero(bvals)[0]
        dwi_ex_array = reorder(len(dwi_idx), n_ex, reverse)
        vol_ex_array = np.array([[i]*n_ex for i in range(len(bvals))])
        for i, ii in enumerate(dwi_idx):
            vol_ex_array[ii, :] = dwi_ex_array[i, :] + (ii-i)
    else:
        raise NotImplementedError("2TRs and 3TRs are not supported yet.")

    new_vol = np.zeros_like(vol)
    for n in range(len(bvals)):
        for z in range(n_ex):
            new_vol[:,:,z,n] = vol[:,:,z,vol_ex_array[n,z]]
    nib.save(nib.Nifti1Image(new_vol, img.affine), out_file)


if __name__ == "__main__":
    fire.Fire(encoding_to_tr)
