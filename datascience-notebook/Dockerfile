FROM nielsbohr/python-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"

USER root

# For opencv2 and basemap geos
RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    libx11-6 \
    libsm6 \
    libxext6 \
    libgeos-dev \
    libglib2.0-0 \
    libxrender1 \
    libgl1-mesa-glx \
    graphviz \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Run container as
USER $NB_UID

# Packages env
ENV BH_CONFIG=$PYTHON2_PATH/lib/python2.7/site-packages/bohrium_api/config.ini

# bohrium_api needs to be present before bohrium install
RUN $PYTHON2_PATH/bin/pip install \
    bohrium_api \
    && $PYTHON3_PATH/bin/pip install \
    bohrium_api

# Install packages for python2/3 envs
RUN $PYTHON2_PATH/bin/pip install \
    numpy \
    bohrium \
    cython \
    opencv-python \
    six \
    nose \
    scipy \
    sympy \
    h5py \
    pandas \
    sklearn \
    seaborn \
    scikit-image \
    pillow \
    mlxtend \
    tqdm \
    pomegranate \
    bokeh \
    Bottleneck \
    dask \
    datashader \
    nbconvert \
    netCDF4 \
    numba \
    statsmodels \
    xarray \
    graphviz \
    pystan \
    pymc3==3.6 \
    pyproj \
    joblib==0.13.0 \
    astropy \
    uncertainties \
    && $PYTHON3_PATH/bin/pip install \
    numpy \
    bohrium \
    cython \
    pandas \
    opencv-python \
    six \
    nose \
    sympy \
    scipy \
    h5py \
    sklearn \
    seaborn \
    scikit-image \
    pillow \
    mlxtend \
    tqdm \
    ruptures \
    pomegranate \
    PyQt5 \
    bokeh \
    Bottleneck \
    dask \
    datashader \
    nbconvert \
    netCDF4 \
    numba \
    statsmodels \
    xarray \
    graphviz \
    pystan \
    pymc3 \
    pyproj \
    joblib==0.13.0 \
    astropy \
    uncertainties

# Matplotlib basemap
RUN $PYTHON2_PATH/bin/pip install git+https://github.com/matplotlib/basemap.git@00794384f59e235f1e2847f952fd08b0bdc4327f \
    && $PYTHON3_PATH/bin/pip install git+https://github.com/matplotlib/basemap.git@00794384f59e235f1e2847f952fd08b0bdc4327f

USER root

RUN fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Run container as
USER $NB_UID
