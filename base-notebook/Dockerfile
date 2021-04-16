# Set default username
FROM jupyter/base-notebook:lab-3.0.12
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60
ARG FACETS_VERSION=0.2.2

USER root

# Setup default timeout of installing packages
RUN echo "[global]" > /etc/pip.conf \
    && echo "timeout=$PACKAGE_TIMEOUT" >> /etc/pip.conf

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    automake \
    autoconf \
    gcc \
    g++ \
    make \
    cmake \
    gfortran \
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
    texlive \
    texlive-latex-extra \
    htop \
    nano \
    vim \
    man \
    less \
    tree \
    rclone \
    unzip \
    wget \
    screen \
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
    'notebook' \
    'ipympl' \
    'ipyleaflet' \
    'ipywidgets' \
    'bqplot' \
    'jupyter_bokeh' \
    'jupyter-server-proxy' \
    'nbgrader' \
    && jupyter labextension install jupyter-leaflet \
                                    @jupyter-widgets/jupyterlab-manager \
                                    bqplot \
                                    @jupyterlab/server-proxy \
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

RUN conda run -n base pip install \
    facets-overview \
    nbresuse \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

RUN conda init \
    && conda config --set auto_activate_base false

# Hide the default $CONDA_DIR/bin/pip to ensure that the user doesn't try to
# install into that one by mistake when it should have been installed into one
# of the jupyter conda environments
RUN mv $CONDA_DIR/bin/pip $CONDA_DIR/bin/jupyterlab_pip \
    && mv $CONDA_DIR/bin/pip3 $CONDA_DIR/bin/jupyterlab_pip3

# Ensure there is a local bin directory for user binaries
RUN mkdir -p ~/.local/bin

ENV PATH="~/.local/bin:$PATH"

USER root

# Script to update the ENV of a particular kernelspec in the image
COPY ./res/update_kernel_spec.py /usr/local/bin/update_kernel_spec.py
RUN chmod +x /usr/local/bin/update_kernel_spec.py

USER $NB_UID

WORKDIR /home/$NB_USER

# Setup the welcome message
COPY ./res/welcome.txt /home/$NB_USER/welcome.txt
RUN cat ~/welcome.txt >> ~/.bashrc \
    && rm -fr /home/$NB_USER/welcome.txt

# Ensure that container Runs as
USER $NB_UID
