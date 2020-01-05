FROM nielsbohr/base-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60

USER root

# Setup default timeout of installing packages
RUN echo "[global]" > /etc/pip.conf \
    && echo "timeout=$PACKAGE_TIMEOUT" >> /etc/pip.conf

ENV PYTHON2_PATH=$CONDA_DIR/envs/python2

USER $NB_UID

WORKDIR /tmp

RUN conda config --set remote_read_timeout_secs $PACKAGE_TIMEOUT

# Install diffpy into python2 env
# diffpy also provides pyobjcrust
RUN conda config --add channels diffpy \
    && conda create -n python2 python=2.7 \
    diffpy-cmi==2.0.1 \
    ipykernel \
    && $PYTHON2_PATH/bin/python -m ipykernel install --user \
    && conda clean --all -f -y \
    && rm -fr /tmp/tmp* \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Ensure that container Runs as
USER $NB_UID

RUN $PYTHON2_PATH/bin/pip install \
    numpy==1.16.4 \
    jupyter-client>=5.3.4 \
    matplotlib \
    six \
    ipython \
    setuptools \
    ase==3.17.0 \
    scipy \
    h5py \
    prompter \
    tqdm \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Ensure $NB_USER uses the conda python envs
RUN mkdir -p /home/$NB_USER/.local/bin

RUN ln -s $PYTHON2_PATH/bin/python /home/$NB_USER/.local/bin/python \
    && ln -s $PYTHON2_PATH/bin/python /home/$NB_USER/.local/bin/python2 \
    && ln -s $PYTHON2_PATH/bin/python /home/$NB_USER/.local/bin/python2.7 \
    && ln -s $PYTHON2_PATH/bin/pip /home/$NB_USER/.local/bin/pip \
    && ln -s $PYTHON2_PATH/bin/pip /home/$NB_USER/.local/bin/pip2 \
    && ln -s $PYTHON2_PATH/bin/pip /home/$NB_USER/.local/bin/pip2.7

RUN jupyter kernelspec uninstall -f python3 \
    && rm -fr $CONDA_DIR/lib/python3.7/site-packages/ipykernel

USER root
RUN rm -r "/home/$NB_USER/.local/share/jupyter/kernels/python2"

RUN sed -i 's/"Python 2"/"Python 2 DiffPy"/g' $PYTHON2_PATH/share/jupyter/kernels/python2/kernel.json \
    && mv $PYTHON2_PATH/share/jupyter/kernels/python2 $PYTHON2_PATH/share/jupyter/kernels/python2_diffpy \
    && cp -r $PYTHON2_PATH/share/jupyter/kernels/python2_diffpy /home/$NB_USER/.local/share/jupyter/kernels/

WORKDIR /home/$NB_USER

# Run container as
USER $NB_UID
