FROM nielsbohr/python-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60

USER root

# Setup default timeout of installing packages
RUN echo "[global]" > /etc/pip.conf \
    && echo "timeout=$PACKAGE_TIMEOUT" >> /etc/pip.conf

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
    # Used in Datf exercises
    fonts-humor-sans \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp

# Run container as
USER $NB_UID

RUN conda config --set remote_read_timeout_secs $PACKAGE_TIMEOUT

# Packages env
ENV BH_CONFIG=$PYTHON2_PATH/lib/python2.7/site-packages/bohrium_api/config.ini

# bohrium_api needs to be present before bohrium install
# Numpy 1.17.* has dropped support of py2
RUN $PYTHON2_PATH/bin/pip install \
    numpy==1.16.4 \
    bohrium_api \
    pystan \
    pymc3==3.6 \
    && $PYTHON3_PATH/bin/pip install \
    bohrium_api \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Install packages for python2/3 envs
RUN $PYTHON2_PATH/bin/pip install \
    bohrium \
    bh107 \
    cython \
    opencv-python \
    six \
    nose \
    scipy \
    sympy \
    h5py \
    pandas \
    sklearn \
    seaborn==0.9.1 \
    scikit-image \
    pillow \
    mlxtend==0.16.0 \
    tqdm \
    pomegranate \
    bokeh \
    Bottleneck \
    dask \
    datashader \
    nbconvert \
    netCDF4 \
    # Last version to support python 2
    llvmlite==0.31.0 \
    # Last version to support python 2
    numba==0.47.0 \
    statsmodels==0.10.2 \
    xarray \
    graphviz \
    pyproj \
    joblib==0.12.5 \
    astropy \
    uncertainties \
    recordclass \
    numdifftools \
    trackpy \
    pims \
    xgboost \
    pydotplus \
    bayesian-optimization==1.0.1 \
    && $PYTHON3_PATH/bin/pip install \
    numpy \
    bohrium \
    bh107 \
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
    joblib==0.13.2 \
    astropy \
    uncertainties \
    recordclass \
    numdifftools \
    trackpy \
    pims \
    xgboost \
    pydotplus \
    bayesian-optimization==1.0.1 \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

## Matplotlib basemap
RUN $PYTHON2_PATH/bin/pip install git+https://github.com/matplotlib/basemap.git@00794384f59e235f1e2847f952fd08b0bdc4327f \
    && $PYTHON3_PATH/bin/pip install git+https://github.com/matplotlib/basemap.git@00794384f59e235f1e2847f952fd08b0bdc4327f

RUN $PYTHON2_PATH/bin/pip install \
    jax \
    jaxlib \
    && $PYTHON3_PATH/bin/pip install \
    jax \
    jaxlib \
    nbi-stat \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

WORKDIR /home/$NB_USER

# Run container as
USER $NB_UID
