FROM nielsbohr/python-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60

USER root

# Setup default timeout of installing packages
RUN echo "[global]" > /etc/pip.conf \
    && echo "timeout=$PACKAGE_TIMEOUT" >> /etc/pip.conf

# For fenics opencv2 and basemap geos
RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    software-properties-common \
    && add-apt-repository ppa:fenics-packages/fenics \
    && apt-get update \
    && apt-get install -yq --no-install-recommends \
    pkg-config \
    libgl1-mesa-glx \
    gmsh \
    libmpfr-dev \
    fenics \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -fr /tmp/tmp*

RUN cd /usr/lib/x86_64-linux-gnu/ \
    && ln -s libmpfr.so /usr/lib/x86_64-linux-gnu/libmpfr.so.4

WORKDIR /tmp

USER $NB_UID

RUN conda config --set remote_read_timeout_secs $PACKAGE_TIMEOUT

ENV LD_LIBRARY_PATH=/opt/conda/lib
ENV PKG_CONFIG_PATH=/opt/conda/envs/python3/lib/pkgconfig

RUN conda install -n python3 \
    fenics \
    && conda clean --all -f -y \
    && rm -fr /tmp/tmp* \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

RUN $PYTHON2_PATH/bin/pip install \
    pygmsh \
    && $PYTHON3_PATH/bin/pip install \
    pygmsh \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

WORKDIR /home/$NB_USER

# Ensure that container Runs as
USER $NB_UID
