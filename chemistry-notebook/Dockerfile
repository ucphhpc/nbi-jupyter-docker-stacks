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

RUN rm -r "/home/$NB_USER/.local/share/jupyter/kernels/python2" \
    "/home/$NB_USER/.local/share/jupyter/kernels/python3" \
    "$CONDA_DIR/share/jupyter/kernels/python3" \
    "$CONDA_DIR/bin/python3"

RUN sed -i 's/"Python 2"/"Python 2 DiffPy"/g' $PYTHON2_PATH/share/jupyter/kernels/python2/kernel.json \
    && mv $PYTHON2_PATH/share/jupyter/kernels/python2 $PYTHON2_PATH/share/jupyter/kernels/python2_diffpy \
    && cp -r $PYTHON2_PATH/share/jupyter/kernels/python2_diffpy /home/$NB_USER/.local/share/jupyter/kernels/

USER $NB_USER
