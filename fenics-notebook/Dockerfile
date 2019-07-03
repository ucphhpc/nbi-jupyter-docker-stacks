FROM nielsbohr/python-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60

USER root

# Setup default timeout of installing packages
RUN echo "[global]" > /etc/pip.conf \
    && echo "timeout=$PACKAGE_TIMEOUT" >> /etc/pip.conf

RUN conda config --set remote_read_timeout_secs $PACKAGE_TIMEOUT

# For opencv2 and basemap geos
RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    pkg-config \
    build-essential \
    libgl1-mesa-glx \
    gmsh \
    libmpfr-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN cd /usr/lib/x86_64-linux-gnu/ \
    && ln -s libmpfr.so /usr/lib/x86_64-linux-gnu/libmpfr.so.4

USER $NB_UID

ENV LD_LIBRARY_PATH=/opt/conda/lib
ENV PKG_CONFIG_PATH=/opt/conda/envs/python3/lib/pkgconfig

RUN conda install -c anaconda -n python2 \
    gcc=4.8 \
    && conda clean -tipsy

RUN conda install -c conda-forge -n python2 \
    fenics=2017.2.0=np113py27_3 \
    && conda clean -tipsy

RUN conda install -c conda-forge -n python3 \
    fenics \
    && conda clean -tipsy

RUN $PYTHON2_PATH/bin/pip install \
    pygmsh

RUN $PYTHON3_PATH/bin/pip install \
    pygmsh

USER root

RUN fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Ensure that container Runs as
USER $NB_UID
