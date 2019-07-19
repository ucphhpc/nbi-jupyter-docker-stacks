# Set default username
FROM jupyter/base-notebook:lab-0.35.5
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
    && rm -rf /tmp/*

# Notebook/Lab dependencies
# dedupe, resolve duplicates packages
# https://ipyleaflet.readthedocs.io/en/latest/installation.html#using-conda
# jupyter-widgets/jupyterlab-manager and matplotlib is for ipympl support which is labs
# replacement for notebook plots
RUN conda install --quiet --yes \
    'ipympl' \
    'ipyleaflet' \
    'ipywidgets' \
    && jupyter labextension install jupyter-leaflet@0.10.8 \
                                    jupyterlab-server-proxy@1.0.0 \
                                    @jupyter-widgets/jupyterlab-manager@0.38 \
                                    jupyter-matplotlib@0.3.0 \
                                    @jupyterlab/celltags@0.1.4 \
                                    jupyterlab_bokeh@0.6.3 \
                                    @pyviz/jupyterlab_pyviz@0.7.2 \
    && conda clean --all -f -y \
    && npm cache clean --force \
    && npm dedupe \
    && rm -rf $CONDA_DIR/share/jupyter/lab/staging \
    && rm -fr /home/$NB_USER/.yarn \
    && rm -fr /home/$NB_USER/.npm \
    && rm -rf /tmp/npm* \
    && rm -fr /tmp/v8*

# Install facets which does not have a pip or conda package at the moment
RUN curl -LOk https://github.com/PAIR-code/facets/archive/${FACETS_VERSION}.tar.gz \
    && tar -xf ${FACETS_VERSION}.tar.gz \
    && cd facets-${FACETS_VERSION} \
    && jupyter nbextension install facets-dist/ --sys-prefix \
    && cd \
    && npm cache clean --force \
    && npm dedupe \
    && cd /tmp \
    && rm -rf $CONDA_DIR/share/jupyter/lab/staging \
    && rm -fr /home/$NB_USER/.yarn \
    && rm -fr /home/$NB_USER/.npm \
    && rm -fr /tmp/facets* \
    && rm -fr /tmp/${FACETS_VERSION}.tar.gz \
    && rm -fr /home/$NB_USER/package-lock.json

USER root

RUN fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

WORKDIR /home/$NB_USER

# Ensure that container Runs as
USER $NB_UID
