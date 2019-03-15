FROM nielsbohr/python-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"

USER root

# For GDAL
RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    g++ \
    software-properties-common \
    && add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable \
    && apt-get update \
    && apt-get install -yq --no-install-recommends \
    gdal-bin \
    libgdal-dev \
    && add-apt-repository --remove ppa:ubuntugis/ubuntugis-unstable \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER $NB_USER

# Use conda since several geo packages
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
    GDAL==2.3.3 \
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
    && conda clean -tipsy \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# RUN conda-env remove -n python3 && \
#     conda create -n python3 python=3.6 ipykernel

# Use conda since several geo packages
RUN conda install -n python3 \
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
    GDAL==2.3.3 \
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
    && conda clean -tipsy \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Run container as
USER $NB_USER