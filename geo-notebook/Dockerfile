FROM nielsbohr/python-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60

USER root

# Setup default timeout of installing packages
RUN echo "[global]" > /etc/pip.conf \
    && echo "timeout=$PACKAGE_TIMEOUT" >> /etc/pip.conf

WORKDIR /tmp

USER $NB_UID

RUN conda config --set remote_read_timeout_secs $PACKAGE_TIMEOUT

# Python2: use conda since several geo packages are only packaged there
RUN conda install -n python2 \
    appmode \
    arrow \
    bokeh \
    bqplot \
    cmocean \
    click \
    cython  \
    cytoolz \
    dask \
    dask-ml as\
    dask-tensorflow \
    datashader \
    distributed \
    esmpy \
    fastparquet \
    geoviews \
    graphviz \
    gsw \
    gdal=2.4.1=py27hf242f0b_3 \
    hvplot \
    intake::intake \
    intake::intake-xarray \
    jedi \
    lz4 \
    msgpack-python \
    nb_conda_kernels \
    netcdf4 \
    nco \
    nomkl \
    numba \
    numcodecs \
    numpy \
    pandas \
    panel \
    python-blosc \
    python-graphviz \
    scipy \
    scikit-image \
    scikit-learn \
    toolz \
    tornado \
    xarray \
    zarr \
    zict \
    rasterio \
    cdo \
    ncl \
    nco \
    && conda clean --all -f -y

# Python3: use conda since several geo packages are only packaged there
RUN conda install -n python3 \
    appmode \
    arrow \
    autopep8 \
    bokeh \
    bqplot \
    cartopy \
    cdo \
    cftime \
    cmocean \
    click \
    colorcet \
    cython  \
    cytoolz \
    dask \
    dask-ml \
    dask-tensorflow \
    datashader \
    distributed \
    eofs \
    esmpy \
    fastparquet \
    flake8 \
    geoviews \
    graphviz \
    gsw \
    GDAL \
    hvplot \
    intake::intake \
    intake::intake-xarray \
    iris \
    jedi \
    libsodium \
    lmfit \
    lz4 \
    msgpack-python \
    nb_conda_kernels \
    netcdf4 \
    nc-time-axis \
    nco \
    nodejs \
    nomkl \
    numba \
    numcodecs \
    numpy \
    palettable \
    pandas \
    panel \
    plotly \
    python-blosc \
    python-graphviz \
    seaborn \
    scipy \
    scikit-image \
    scikit-learn \
    statsmodels \
    toolz \
    tornado \
    xarray \
    xesmf \
    zarr \
    zict \
    rasterio \
    cdo \
    ncl \
    nco \
    && conda clean --all -f -y

# Finally install any remaining packages with pip
RUN $PYTHON3_PATH/bin/pip install \
    schemdraw

USER root

RUN fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

WORKDIR /home/$NB_USER

# Ensure that container Runs as
USER $NB_UID
