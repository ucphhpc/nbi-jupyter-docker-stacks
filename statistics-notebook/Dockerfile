FROM nielsbohr/python-notebook:latest
MAINTAINER Rasmus Munk <rasmus.munk@nbi.ku.dk>

USER root

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    g++ \
    graphviz \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Run container as
USER $NB_USER

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
    pymc3 \
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
    pymc3 \
    && fix-permissions $CONDA_DIR

RUN git clone git://github.com/scikit-hep/probfit.git \
    && cd probfit \
    && $PYTHON2_PATH/bin/pip install cython \
    && $PYTHON2_PATH/bin/pip install . \
    && $PYTHON3_PATH/bin/pip install cython \
    && $PYTHON3_PATH/bin/pip install .
