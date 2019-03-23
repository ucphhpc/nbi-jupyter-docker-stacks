FROM nielsbohr/python-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"

USER root

# For GDAL
RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    g++ \
    software-properties-common \
    nano vim git \
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
    GDAL==2.3.3 \
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
    && conda clean -tipsy \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

RUN $PYTHON3_PATH/bin/pip install \
    schemdraw

RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager \
                                     @jupyterlab/hub-extension \
                                     @pyviz/jupyterlab_pyviz \
                                     jupyter-leaflet \
                                     jupyterlab_bokeh \
                                     dask-labextension \
				     jupyterlab-server-proxy

# Run container as
USER $NB_USER
