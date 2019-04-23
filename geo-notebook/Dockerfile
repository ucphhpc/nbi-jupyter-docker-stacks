FROM nielsbohr/python-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"

USER $NB_USER
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
    dask-ml \
    dask-tensorflow \
    datashader \
    distributed \
    esmpy \
    fastparquet \
    geoviews \
    graphviz \
    gsw \
    GDAL \
    hvplot \
    intake::intake \
    intake::intake-xarray \
    jedi \
    lz4 \
    msgpack-python \
    nb_conda_kernels \
    nbserverproxy \
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
    xesmf \
    zarr \
    zict \
    rasterio \
    cdo \
    ncl \
    nco \
    && conda clean -tipsy \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

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
    && conda clean -tipsy \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Finally install any remaining packages with pip
RUN $PYTHON3_PATH/bin/pip install \
    schemdraw \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Run container as
USER $NB_USER
