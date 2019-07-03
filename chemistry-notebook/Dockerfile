FROM nielsbohr/python-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG LIBCRYST_VERSION="2017.2.1"
ARG PACKAGE_TIMEOUT=60

USER root

# Setup default timeout of installing packages
RUN echo "[global]" > /etc/pip.conf \
    && echo "timeout=$PACKAGE_TIMEOUT" >> /etc/pip.conf

RUN conda config --set remote_read_timeout_secs $PACKAGE_TIMEOUT

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    libboost-dev \
    scons \
    g++ \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Get libobjcrsyt source for building
RUN curl -LOk https://github.com/diffpy/libobjcryst/releases/download/v2017.2.1/libobjcryst-2017.2.1.tar.gz \
    && tar xzf "libobjcryst-$LIBCRYST_VERSION.tar.gz" \
    && cd "libobjcryst-$LIBCRYST_VERSION" \
    &&  scons -j4 install

USER $NB_UID

# Clearout other kernels
RUN conda remove --name python3 --all

# Install diffpy into python2 env
RUN conda config --add channels diffpy \
    && conda install -n python2 diffpy-cmi libobjcryst \
    && conda clean -tipsy

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
    pyobjcryst \
    h5py \
    prompter \
    tqdm \
    diffpy.srfit

# RUN cd /tmp \
#     && git clone https://github.com/diffpy/diffpy.srfit.git \
#     && cd diffpy.srfit \
#     && $PYTHON2_PATH/bin/python setup.py install \
#     && rm -r /tmp/diffpy.srfit \
#     && fix-permissions $CONDA_DIR \
#     && fix-permissions /home/$NB_USER

RUN rm -r "/home/$NB_USER/.local/share/jupyter/kernels/python2" \
    "/home/$NB_USER/.local/share/jupyter/kernels/python3" \
    "$CONDA_DIR/share/jupyter/kernels/python3" \
    "$CONDA_DIR/bin/python3"

RUN sed -i 's/"Python 2"/"Python 2 DiffPy"/g' $PYTHON2_PATH/share/jupyter/kernels/python2/kernel.json \
    && mv $PYTHON2_PATH/share/jupyter/kernels/python2 $PYTHON2_PATH/share/jupyter/kernels/python2_diffpy \
    && cp -r $PYTHON2_PATH/share/jupyter/kernels/python2_diffpy /home/$NB_USER/.local/share/jupyter/kernels/

USER root

RUN fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Ensure that container Runs as
USER $NB_UID
