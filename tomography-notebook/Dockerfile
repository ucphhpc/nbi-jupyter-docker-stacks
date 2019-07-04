FROM nielsbohr/python-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60

USER root

# Setup default timeout of installing packages
RUN echo "[global]" > /etc/pip.conf \
    && echo "timeout=$PACKAGE_TIMEOUT" >> /etc/pip.conf

RUN conda config --set remote_read_timeout_secs $PACKAGE_TIMEOUT

# RUN apt-get update \
#     && apt-get install -yq --no-install-recommends \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# Run container as
USER $NB_UID

# Packages env
ENV BH_CONFIG=$PYTHON2_PATH/lib/python2.7/site-packages/bohrium_api/config.ini

RUN conda create -n astra -c astra-toolbox \
    astra-toolbox \
    && conda clean -tipsy

# Install packages for python2/3 envs
RUN $PYTHON2_PATH/bin/pip install \
    numpy \
    bohrium \
    scipy \
    h5py \
    pandas \
    sklearn \
    seaborn \
    scikit-image \
    pillow \
    tqdm \
    netCDF4 \
    graphviz \
    matplotlib \
    && $PYTHON3_PATH/bin/pip install \
    numpy \
    bohrium \
    scipy \
    h5py \
    pandas \
    sklearn \
    seaborn \
    scikit-image \
    pillow \
    tqdm \
    netCDF4 \
    graphviz \
    matplotlib

USER root

RUN fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Run container as
USER $NB_UID
