FROM nielsbohr/python-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"

USER $NB_USER

# Install diffpy
ENV PYTHON2_DIFFPY_PATH=$CONDA_DIR/envs/python2_diffpy

RUN conda create -n python2_diffpy python=2.7 ipykernel \
    && conda config --add channels diffpy \
    && conda install -n python2_diffpy diffpy-cmi diffpy- \
    && conda clean -tipsy \
    && fix-permissions $CONDA_DIR \
    && sed -i 's/"Python 2"/"Python 2 DiffPy"/g' $PYTHON2_DIFFPY_PATH/share/jupyter/kernels/python2/kernel.json \
    && mv $PYTHON2_DIFFPY_PATH/share/jupyter/kernels/python2 $PYTHON2_DIFFPY_PATH/share/jupyter/kernels/python2_diffpy \
    && cp -r $PYTHON2_DIFFPY_PATH/share/jupyter/kernels/python2_diffpy /home/$NB_USER/.local/share/jupyter/kernels/

RUN $PYTHON2_DIFFPY_PATH/bin/pip install \
    numpy \
    matplotlib \
    six \
    ipython \
    pyobjcryst \
    h5py \
    prompter \
    tqdm \
    ase \
    && fix-permissions $CONDA_DIR

USER $NB_USER
