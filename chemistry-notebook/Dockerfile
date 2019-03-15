FROM nielsbohr/python-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG LIBCRYST_VERSION="2017.2.1"

USER root

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    libboost-dev \
    scons \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Get libobjcrsyt source for building
RUN curl -LOk https://github.com/diffpy/libobjcryst/releases/download/v2017.2.1/libobjcryst-2017.2.1.tar.gz \
    && tar xzf "libobjcryst-$LIBCRYST_VERSION.tar.gz" \
    && cd "libobjcryst-$LIBCRYST_VERSION" \
    &&  scons -j4 install

USER $NB_USER

# Clearout other kernels
RUN conda remove --name python3 --all

# Install diffpy into python2 env
RUN conda config --add channels diffpy \
    && conda install -n python2 diffpy-cmi libobjcryst \
    && conda clean -tipsy \
    && fix-permissions $CONDA_DIR

# Get rid of old matplotlib
RUN $PYTHON2_PATH/bin/pip uninstall -y \
    matplotlib

RUN $PYTHON2_PATH/bin/pip install -U \
    numpy \
    matplotlib \
    six \
    ipython \
    setuptools \
    ase \
    scipy \
    pyobjcryst==2.0.2 \
    h5py \
    prompter \
    tqdm \
    && fix-permissions $CONDA_DIR

RUN cd /tmp \
    && git clone https://github.com/diffpy/diffpy.srfit.git \
    && cd diffpy.srfit \
    && $PYTHON2_PATH/bin/python setup.py install \
    && rm -r /tmp/diffpy.srfit

RUN rm -r "/home/$NB_USER/.local/share/jupyter/kernels/python2" \
    "/home/$NB_USER/.local/share/jupyter/kernels/python3" \
    "$CONDA_DIR/share/jupyter/kernels/python3" \
    "$CONDA_DIR/bin/python3"

RUN sed -i 's/"Python 2"/"Python 2 DiffPy"/g' $PYTHON2_PATH/share/jupyter/kernels/python2/kernel.json \
    && mv $PYTHON2_PATH/share/jupyter/kernels/python2 $PYTHON2_PATH/share/jupyter/kernels/python2_diffpy \
    && cp -r $PYTHON2_PATH/share/jupyter/kernels/python2_diffpy /home/$NB_USER/.local/share/jupyter/kernels/

USER $NB_USER
