# -*- coding: utf-8 -*-
#
# Script based on Nilearn Example 03, see
# https://nilearn.github.io/stable/auto_examples/03_connectivity/plot_inverse_covariance_connectome.html#compute-the-sparse-inverse-covariance
#

from nilearn import datasets
atlas = datasets.fetch_atlas_msdl()
# Loading atlas image stored in 'maps'
atlas_filename = atlas['maps']
# Loading atlas data stored in 'labels'
labels = atlas['labels']

# Loading the functional datasets
data = datasets.fetch_development_fmri(n_subjects=1)

# print basic information on the dataset
print('First subject functional nifti images (4D) are at: %s' %
      data.func[0])  # 4D data
