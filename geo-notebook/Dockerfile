FROM nielsbohr/datascience-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"

USER root

# For GDAL
RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    proj-bin \
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

# The following was used from
# https://raw.githubusercontent.com/rsignell-usgs/helm-chart/conda-forge/docker-images/notebook/Dockerfile
RUN apt-get update \
  && apt-get install -yq --no-install-recommends \
         libfuse-dev nano fuse vim git man tree \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

USER $NB_USER

RUN conda update conda --yes \
  && conda config --remove channels defaults

RUN conda install --yes \
    appmode \
    arrow \
    bokeh \
    bqplot \
    cartopy \
    cdo \
    cftime \
    cmocean \
    click \
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
    && conda clean -tipsy

RUN $PYTHON3_PATH/bin/pip install \
    schemdraw

RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager \
                                     @jupyterlab/hub-extension \
                                     @pyviz/jupyterlab_pyviz \
                                     jupyter-leaflet \
                                     jupyterlab_bokeh \
                                     dask-labextension \
				     jupyterlab-server-proxy

RUN python -m ipykernel install --user
