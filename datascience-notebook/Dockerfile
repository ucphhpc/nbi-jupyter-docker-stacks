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
    # HDF5 and netCDF4 requirements
    libhdf5-dev \
    libhdf5-doc \
    libnetcdf-dev \
    libnetcdff-dev \
    libnetcdff-doc \
    libx11-6 \
    libsm6 \
    libxext6 \
    libgeos-dev \
    libglib2.0-0 \
    libxrender1 \
    libgl1-mesa-glx \
    graphviz \
    # Required by cartopy
    libproj-dev \
    proj-data \
    proj-bin \
    libgeos-dev \
    # Used in Datf exercises
    fonts-humor-sans \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp

USER $NB_UID

RUN conda config --set remote_read_timeout_secs $PACKAGE_TIMEOUT

# Proj4 is required for cartopy
RUN conda install -n python3 \
    proj4 \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Install packages for python3 envs
COPY requirements.txt /tmp/
RUN conda run -n python3 pip install -r requirements.txt \
    && conda clean -y --all \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Matplotlib basemap
RUN $PYTHON3_PATH/bin/pip install git+https://github.com/matplotlib/basemap.git@3076ec9470cf7dba523bc94ebe5ae9a990e34d08

WORKDIR /home/$NB_USER

# Run container as
USER $NB_UID
