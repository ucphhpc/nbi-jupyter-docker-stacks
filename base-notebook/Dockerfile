# Set default username
FROM jupyter/base-notebook:lab-1.2.1
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60
ARG FACETS_VERSION=0.2.2

USER root

# Setup default timeout of installing packages
RUN echo "[global]" > /etc/pip.conf \
    && echo "timeout=$PACKAGE_TIMEOUT" >> /etc/pip.conf

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    gcc \
    g++ \
    make \
    perl \
    tar \
    bzip2 \
    zlib1g \
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
    vim \
    man \
    less \
    tree \
    rclone \
    unzip \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN chown $NB_UID:$NB_GID -R /tmp

WORKDIR /tmp

USER $NB_UID

RUN conda config --set remote_read_timeout_secs $PACKAGE_TIMEOUT

# Environement variables
ENV CONDA_DIR=/opt/conda
ENV JUPYTER_PATH=$CONDA_DIR/envs/jupyter

# Don't install development junk
RUN npm config set production

# Update conda, npm, yarn
RUN conda update --quiet -n base conda \
    && npm i -g npm \
    && npm i -g yarn \
    && conda clean --all -f -y \
    && npm cache clean --force \
    && rm -fr /home/$NB_USER/.yarn \
    && rm -fr /home/$NB_USER/.npm \
    && rm -fr /home/$NB_USER/.node \
    && rm -fr /home/$NB_USER/.npmrc \
    && rm -rf /tmp/* \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Notebook/Lab dependencies
# dedupe, resolve duplicates packages
# https://ipyleaflet.readthedocs.io/en/latest/installation.html#using-conda
# jupyter-widgets/jupyterlab-manager and matplotlib is for ipympl support which is labs
# replacement for notebook plots
# https://github.com/yuvipanda/jupyter-launcher-shortcuts
RUN conda install --quiet --yes \
    'notebook==6.0.2' \
    'ipympl' \
    'ipyleaflet' \
    'ipywidgets' \
    'bqplot' \
    'jupyter-server-proxy' \
    && jupyter labextension install jupyter-leaflet@0.11.6 \
                                    @jupyter-widgets/jupyterlab-manager@1.1.0 \
                                    jupyterlab_bokeh@1.0.0 \
                                    @pyviz/jupyterlab_pyviz@0.8.0 \
                                    bqplot@0.5.2 \
                                    @jupyterlab/server-proxy@2.0.0 \
                                    jupyterlab-topbar-extension \
                                    jupyterlab-system-monitor \
    && conda clean --all -f -y \
    && npm cache clean --force \
    && npm dedupe \
    && rm -rf $CONDA_DIR/share/jupyter/lab/staging \
    && rm -rf $CONDA_DIR/share/jupyter/lab/extensions/jupyter-matplotlib-0.4.0.tgz \
    && rm -fr $CONDA_DIR/share/jupyter/lab/extensions/jupyter-matplotlib-0.4.1.tgz \
    && rm -fr /home/$NB_USER/.yarn \
    && rm -fr /home/$NB_USER/.npm \
    && rm -rf /tmp/npm* \
    && rm -fr /tmp/v8* \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

RUN $CONDA_DIR/bin/pip install \
    facets-overview \
    nbresuse \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

WORKDIR /home/$NB_USER

# Ensure that container Runs as
USER $NB_UID
