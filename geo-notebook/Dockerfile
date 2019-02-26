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

RUN conda install --yes  \
    appmode \
    arrow \
    bokeh \
    bqplot \
    cartopy \
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
    libsodium \
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
    && conda clean -tipsy

RUN $PYTHON3_PATH/bin/pip install \
    nc_time_axis \
    schemdraw

RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager \
                                     @jupyterlab/hub-extension \
                                     @pyviz/jupyterlab_pyviz \
                                     jupyter-leaflet \
                                     jupyterlab_bokeh \
                                     dask-labextension

RUN jupyter serverextension enable --py nbserverproxy jupyterlab --sys-prefix


RUN python -m ipykernel install --user
