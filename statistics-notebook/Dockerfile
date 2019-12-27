FROM nielsbohr/python-notebook:edge
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60

USER root

# Setup default timeout of installing packages
RUN echo "[global]" > /etc/pip.conf \
    && echo "timeout=$PACKAGE_TIMEOUT" >> /etc/pip.conf

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    graphviz \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp

# Run container as
USER $NB_UID

RUN conda config --set remote_read_timeout_secs $PACKAGE_TIMEOUT

RUN $PYTHON2_PATH/bin/pip install \
    numpy==1.16.4 \
    bohrium_api \
    pystan \
    pymc3==3.6 \
    && $PYTHON3_PATH/bin/pip install \
    bohrium_api \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Install packages for python2/3 envs
RUN $PYTHON2_PATH/bin/pip install \
    bohrium \
    scipy \
    seaborn \
    sklearn \
    pandas \
    iminuit \
    graphviz \
    ipywidgets \
    && $PYTHON3_PATH/bin/pip install \
    numpy \
    bohrium \
    scipy \ 
    seaborn \
    sklearn \
    pandas \
    iminuit \
    graphviz \
    ipywidgets \
    pystan \
    pymc3 \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

RUN git clone https://github.com/scikit-hep/probfit.git \
    && cd probfit \
    && git checkout 6c64dd6d46c4155f83e2a75eead17e66d829911f \
    && $PYTHON2_PATH/bin/pip install cython \
    && $PYTHON2_PATH/bin/pip install . \
    && $PYTHON3_PATH/bin/pip install cython \
    && $PYTHON3_PATH/bin/pip install . \
    && rm -fr /tmp/probfit \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

USER root

WORKDIR /home/$NB_USER

# Ensure that container Runs as
USER $NB_UID
