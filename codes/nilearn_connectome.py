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

# Remove subjects for which partial correlation computation diverges
subjectList = list(set(range(33)).difference([7,8,11,12,19,21,22,23,24,26,27,28]))

def compute_connectome(subIdx):

    # Take stock of data on disk
    data = datasets.fetch_development_fmri(age_group="adult",
                                           data_dir="/cs/home/fuertingers/nilearn_data")
    atlas = datasets.fetch_coords_power_2011(legacy_format=False)
    atlasCoords = np.vstack((atlas.rois['x'], atlas.rois['y'], atlas.rois['z'])).T

    # Extract fMRI time-series averaged within spheres @ atlas coords
    masker = NiftiSpheresMasker(seeds=atlasCoords, smoothing_fwhm=6, radius=5., detrend=True, standardize=True,
                                low_pass=0.1, high_pass=0.01, t_r=2)
    timeseries = masker.fit_transform(data.func[subIdx], confounds=data.confounds[subIdx])

    # Compute functional connectivity b/w brain regions
    estimator = GraphicalLassoCV()
    estimator.fit(timeseries)
    return estimator.covariance_


if __name__ == "__main__":

    # What subject do we want to analyze?
    subjectIdx = 5

    # On disk location of data and results
    dataDir = "/cs/home/fuertingers/nilearn_data"
    resDir = "/cs/home/fuertingers/nilearn_results"

    # Compute functional connectivity of subject
    con = compute_connectome(subjectIdx)

    # Show results
    fig = plt.figure()
    plotting.plot_connectome(con, coords, title='Subject #{}'.format(subjectIdx),
                                  edge_threshold='95%', node_size=20, colorbar=True,
                                  edge_vmin=-1, edge_vmax=1, figure=fig)
    fig.savefig(os.path.join(resDir, "subject{}.png".format(subjectIdx)))
    view = plotting.view_connectome(con, coords, edge_threshold="95%")
    view.open_in_browser(os.path.join(resDir, "subject{}.html".format(subjectIdx)))
