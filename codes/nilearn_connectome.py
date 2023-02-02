# -*- coding: utf-8 -*-
#
# Script based on Nilearn Example 03, see
# https://nilearn.github.io/stable/auto_examples/03_connectivity/plot_inverse_covariance_connectome.html#compute-the-sparse-inverse-covariance
#

import os
from nilearn import datasets, plotting
from nilearn.maskers import NiftiSpheresMasker
from sklearn.covariance import GraphicalLassoCV
import matplotlib.pyplot as plt
import numpy as np

# # Global directory for NiLearn datasets
# dataDir = "/cs/home/fuertingers/nilearn_data"

# # Loading atlas image stored in 'maps'
# atlas = datasets.fetch_atlas_msdl(data_dir=dataDir)

# # Loading atlas data stored in 'labels'
# labels = atlas['labels']
# atlas_filename = atlas['maps']

# # Loading the functional datasets
# data = datasets.fetch_development_fmri(age_group="adult", data_dir=dataDir)
# atlas = datasets.fetch_coords_power_2011(legacy_format=False)
# coords = np.vstack((atlas.rois['x'], atlas.rois['y'], atlas.rois['z'])).T

# # print basic information on the dataset
# print('First subject functional nifti images (4D) are at: %s' %
#       data.func[0])  # 4D data

def compute_connectome(subjectIdx, coords, dataDir):

      # Take stock of data on disk
      data = datasets.fetch_development_fmri(age_group="adult", data_dir=dataDir)

      # Extract fMRI time-series averaged within spheres centered at atlas coordinates
      spheres_masker = NiftiSpheresMasker(seeds=coords, smoothing_fwhm=6, radius=5.,
                                          detrend=True, standardize=True, low_pass=0.1,
                                          high_pass=0.01, t_r=2)
      timeseries = spheres_masker.fit_transform(data.func[subjectIdx],
                                                confounds=data.confounds[subjectIdx])

      # Compute functional connectivity b/w brain regions
      estimator = GraphicalLassoCV()
      estimator.fit(timeseries)

      return estimator.covariance_

if __name__ == "__main__":

      # What subject do we want to analyze?
      subjectIdx = 0

      # On disk location of data and results
      dataDir = "/cs/home/fuertingers/nilearn_data"
      resDir = "/cs/home/fuertingers/nilearn_results"

      # Load atlas from Power et al., 2011 and extract CoM coordinates
      atlas = datasets.fetch_coords_power_2011(legacy_format=False)
      coords = np.vstack((atlas.rois['x'], atlas.rois['y'], atlas.rois['z'])).T

      # Compute functional connectivity of subject
      con = compute_connectome(subjectIdx, coords, dataDir)

      # Show results
      fig = plt.figure()
      plotting.plot_connectome(con, coords, title='Subject #{}'.format(subjectIdx),
                               edge_threshold='95%', node_size=20, colorbar=True,
                               edge_vmin=-1, edge_vmax=1, figure=fig)
      fig.savefig(os.path.join(resDir, "subject{}.png".format(subjectIdx)))
      view = plotting.view_connectome(con, coords, edge_threshold="95%")
      view.open_in_browser(os.path.join(resDir, "subject{}.html".format(subjectIdx)))
