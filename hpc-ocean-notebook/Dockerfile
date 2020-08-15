FROM nielsbohr/slurm-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    libnetcdf-dev \
    libnetcdff-dev \
    libnetcdff-doc \
    && apt-get clean \
    && rm -fr /var/lib/apt/lists/*

RUN apt-get update \
    && apt-get install -y libhdf5-dev libnetcdf-dev \
    && ln -s /usr/include/hdf5/serial /usr/include/hdf5/include

ENV HDF5_DIR="/usr/include/hdf5"

RUN $PYTHON2_PATH/bin/pip install \
    scipy==1.2.2 \
    jax \
    jaxlib \
    bohrium \
    veros \
    tensorflow \
    && $PYTHON3_PATH/bin/pip install \
    numpy==1.18.4 \
    scipy==1.4.1 \
    botorch \
    jax \
    jaxlib \
    bohrium \
    veros \
    tensorflow \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Run container as
USER $NB_UID
