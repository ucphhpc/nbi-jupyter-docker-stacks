FROM nielsbohr/base-notebook:latest
MAINTAINER Rasmus Munk <rasmus.munk@nbi.ku.dk>

USER root

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER $NB_USER

# Environment variables
ENV BH_CONFIG=/home/$NB_USER/.local/lib/python2.7/site-packages/bohrium/config.ini
ENV PYTHON2_PATH=$CONDA_DIR/envs/python2
ENV PYTHON3_PATH=$CONDA_DIR/envs/python3

# Create user python2/3 environement
RUN conda create -n python2 python=2 ipykernel \
    && conda create -n python3 python=3 ipykernel \
    && $PYTHON2_PATH/bin/python -m ipykernel install --user \
    && $PYTHON3_PATH/bin/python -m ipykernel install --user \
    && conda clean -tipsy \
    && fix-permissions $CONDA_DIR

# upgrade pip
RUN $PYTHON2_PATH/bin/pip install --upgrade pip setuptools \
    && $PYTHON3_PATH/bin/pip install --upgrade pip setuptools

# Install bohrium/matplotlib/pandas/scikit-image for py2/py3
RUN $PYTHON2_PATH/bin/pip install --no-cache-dir numpy==1.14.5 \
    && $PYTHON2_PATH/bin/pip install --no-cache-dir --user bohrium \
    && $PYTHON2_PATH/bin/pip install --no-cache-dir \
    scikit-image \
    pandas \
    sklearn \
    ipyleaflet \
    ipywidgets \
    soundfile \
    autopep8 \
    sympy \
    tqdm \
    tensorflow \
    keras \
    peakutils \
    opencv-python \
    && $PYTHON3_PATH/bin/pip install --no-cache-dir numpy==1.14.5 \
    && $PYTHON3_PATH/bin/pip install --no-cache-dir --user bohrium \
    && $PYTHON3_PATH/bin/pip install --no-cache-dir \
    scikit-image \
    pandas \
    sklearn \
    ipyleaflet \
    ipywidgets \
    soundfile \
    autopep8 \
    sympy \
    tqdm \
    tensorflow \
    keras \
    peakutils \
    opencv-python \
    && fix-permissions $CONDA_DIR

# Set the default python terminal links to the used kernels
# Don't delete native python3.6 -> required when spawned
RUN mv $CONDA_DIR/bin/python3.6 $CONDA_DIR \
    && rm $CONDA_DIR/bin/python* \
    $CONDA_DIR/bin/pip* \
    && mv $CONDA_DIR/python3.6 $CONDA_DIR/bin/ \
    && ln -s $CONDA_DIR/bin/python3.6 $CONDA_DIR/bin/python \
    && ln -s $PYTHON2_PATH/bin/python $CONDA_DIR/bin/python2 \
    && ln -s $PYTHON3_PATH/bin/python3 $CONDA_DIR/bin/python3 \
    && ln -s $PYTHON2_PATH/bin/pip $CONDA_DIR/bin/pip \
    && ln -s $PYTHON3_PATH/bin/pip $CONDA_DIR/bin/pip3

# Run container as
USER $NB_USER