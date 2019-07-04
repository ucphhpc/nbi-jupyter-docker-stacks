# Set default username
FROM jupyter/base-notebook:lab-0.35.5
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60

USER root

# Setup default timeout of installing packages
RUN echo "[global]" > /etc/pip.conf \
    && echo "timeout=$PACKAGE_TIMEOUT" >> /etc/pip.conf

RUN conda config --set remote_read_timeout_secs $PACKAGE_TIMEOUT

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    build-essential \
    git \
    tzdata \
    lftp \
    openssh-client \
    rsync \
    curl \
    texlive-xetex \
    texlive-generic-recommended \
    texlive-fonts-recommended \
    htop \
    nano \
    man \
    tree \
    vim \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# rclone install
RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    unzip \
    p7zip-full \
    busybox \
    man-db \
    && curl https://rclone.org/install.sh | bash \
    && apt-get remove -yq \
    unzip \
    p7zip-full \
    busybox \
    man-db \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER $NB_UID

# Environement variables
ENV CONDA_DIR=/opt/conda

WORKDIR /tmp

# Update conda, npm, yarn
RUN conda update -n base conda \
    && npm i -g npm \
    && npm i -g yarn

# Upgrade underlying pip that jlab uses
RUN pip install --upgrade pip

# Notebook/Lab dependencies,
# dedupe, resolve duplicates packages
# https://ipyleaflet.readthedocs.io/en/latest/installation.html#using-conda
# jupyter-widgets/jupyterlab-manager and matplotlib is for ipympl support which is labs
# replacement for notebook plots
RUN conda install --quiet --yes \
    'ipympl' \
    'ipyleaflet' \
    && jupyter labextension install jupyter-leaflet@0.10.8 \
                                    jupyterlab-server-proxy@1.0.0 \
                                    @jupyter-widgets/jupyterlab-manager@0.38 \
                                    jupyter-matplotlib@0.3.0 \
                                    @jupyterlab/celltags@0.1.4 \
                                    jupyterlab_bokeh@0.6.3 \
                                    @pyviz/jupyterlab_pyviz@0.7.2 \
    && npm dedupe \
    && npm cache clean --force \
    && rm -rf /home/$NB_USER/.cache/yarn \
    && rm -rf /home/$NB_USER/.node-gyp

## Install facets which does not have a pip or conda package at the moment
RUN git clone https://github.com/PAIR-code/facets.git \
    && cd facets \
    && jupyter nbextension install facets-dist/ --sys-prefix \
    && cd \
    && rm -rf /tmp/facets

USER root

RUN fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Ensure that container Runs as
USER $NB_UID

WORKDIR /home/$NB_USER
