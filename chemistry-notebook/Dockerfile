FROM nielsbohr/python-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"

USER $NB_USER

# Clearout other kernels

RUN conda remove --name python3 --all

# Install diffpy into python2 env
RUN conda config --add channels diffpy \
    && conda install -n python2 diffpy-cmi \
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
    pyobjcryst \
    h5py \
    prompter \
    tqdm \
    && fix-permissions $CONDA_DIR

RUN cd /tmp \
    && git clone https://github.com/diffpy/diffpy.srfit.git \
    && cd diffpy.srfit \
    && $PYTHON2_PATH/bin/python setup.py install \
    && rm -r /tmp/diffpy.srfit

RUN rm -r "/home/$NB_USER/.local/share/jupyter/kernels/python3" \
    "$CONDA_DIR/share/jupyter/kernels/python3" \
    "$CONDA_DIR/bin/python" \
    "$CONDA_DIR/bin/python3" 

RUN ln -s $PYTHON2_PATH/bin/python $CONDA_DIR/bin/python

USER $NB_USER
