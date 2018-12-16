FROM nielsbohr/base-notebook:latest
MAINTAINER Rasmus Munk <rasmus.munk@nbi.ku.dk>

USER root

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    gcc \
    python-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER $NB_USER

ENV PYTHON2_PATH=$CONDA_DIR/envs/python2
ENV PYTHON3_PATH=$CONDA_DIR/envs/python3

# Create user python2/3 environement
RUN conda create -n python2 python=2.7 ipykernel \
    && conda create -n python3 python=3.6 ipykernel \
    && $PYTHON2_PATH/bin/python -m ipykernel install --user \
    && $PYTHON3_PATH/bin/python -m ipykernel install --user \
    && conda clean -tipsy \
    && fix-permissions $CONDA_DIR

# upgrade pip
RUN $PYTHON2_PATH/bin/pip install --upgrade pip setuptools \
    && $PYTHON3_PATH/bin/pip install --upgrade pip setuptools

# Add matplotlib widget for jlab
RUN $PYTHON2_PATH/bin/pip install \
    ipympl \
    ipyleaflet \
    ipywidgets \
    && $PYTHON3_PATH/bin/pip install \
    ipympl \
    ipyleaflet \
    ipywidgets \
    && fix-permissions $CONDA_DIR

# Set the default python terminal links to the used kernels
# Don't delete native python3.7 -> required when spawned
RUN mv $CONDA_DIR/bin/python3.7 $CONDA_DIR \
    && rm $CONDA_DIR/bin/python* \
    $CONDA_DIR/bin/pip* \
    && mv $CONDA_DIR/python3.7 $CONDA_DIR/bin/ \
    && ln -s $CONDA_DIR/bin/python3.7 $CONDA_DIR/bin/python \
    && ln -s $PYTHON2_PATH/bin/python $CONDA_DIR/bin/python2 \
    && ln -s $PYTHON3_PATH/bin/python3 $CONDA_DIR/bin/python3 \
    && ln -s $PYTHON2_PATH/bin/pip $CONDA_DIR/bin/pip \
    && ln -s $PYTHON3_PATH/bin/pip $CONDA_DIR/bin/pip3

# Run container as
USER $NB_USER