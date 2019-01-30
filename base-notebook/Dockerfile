# Set default username
FROM jupyter/base-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"

USER root

RUN apt-get update \
    && apt-get -yq dist-upgrade \
    && apt-get install -yq --no-install-recommends \
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

USER $NB_USER

# Environement variables
ENV CONDA_DIR=/opt/conda

WORKDIR /tmp

# Update conda, npm, yarn
RUN conda update -n base conda \
    && npm i -g npm \
    && npm i -g yarn

# Update conda packages (such as notebook, jlab, jhub)
RUN conda update --quiet --yes --all

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
    && jupyter labextension install jupyter-leaflet \
    && jupyter labextension install @jupyter-widgets/jupyterlab-manager \
    && jupyter labextension install jupyter-matplotlib \
    && jupyter labextension install @jupyterlab/celltags \
    && npm dedupe \
    && npm cache clean --force \
    && rm -rf /home/$NB_USER/.cache/yarn \
    && rm -rf /home/$NB_USER/.node-gyp \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

## Install facets which does not have a pip or conda package at the moment
RUN git clone https://github.com/PAIR-code/facets.git \
    && cd facets \
    && jupyter nbextension install facets-dist/ --sys-prefix \
    && cd \
    && rm -rf /tmp/facets \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

WORKDIR /home/$NB_USER

# Ensure that container Runs as
USER $NB_USER