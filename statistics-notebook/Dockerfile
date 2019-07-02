FROM nielsbohr/python-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"

USER root

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    g++ \
    graphviz \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Run container as
USER $NB_UID

# Install packages for python2/3 envs
RUN $PYTHON2_PATH/bin/pip install \
    numpy \
    matplotlib \
    scipy \
    seaborn \
    sklearn \
    pandas \
    iminuit \
    graphviz \
    ipywidgets \
    pystan \
    pymc3==3.6 \
    && $PYTHON3_PATH/bin/pip install \
    numpy \
    matplotlib \
    scipy \ 
    seaborn \
    sklearn \
    pandas \
    iminuit \
    graphviz \
    ipywidgets \
    pystan \
    pymc3

RUN git clone https://github.com/scikit-hep/probfit.git \
    && cd probfit \
    && git checkout 6c64dd6d46c4155f83e2a75eead17e66d829911f \
    && $PYTHON2_PATH/bin/pip install cython \
    && $PYTHON2_PATH/bin/pip install . \
    && $PYTHON3_PATH/bin/pip install cython \
    && $PYTHON3_PATH/bin/pip install .

USER root

RUN fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Ensure that container Runs as
USER $NB_UID
