FROM nielsbohr/python-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60

USER root

# Setup default timeout of installing packages
RUN echo "[global]" > /etc/pip.conf \
    && echo "timeout=$PACKAGE_TIMEOUT" >> /etc/pip.conf

WORKDIR /tmp

# Run container as
USER $NB_UID

RUN conda config --set remote_read_timeout_secs $PACKAGE_TIMEOUT

# Packages env
ENV BH_CONFIG=$PYTHON2_PATH/lib/python2.7/site-packages/bohrium_api/config.ini
ENV ASTRA_PATH=$CONDA_DIR/envs/astra

RUN conda create -n astra -c astra-toolbox/label/dev \
    astra-toolbox \
    ipykernel \
    && $ASTRA_PATH/bin/python -m ipykernel install --user --name astra \
    && conda clean --all -f -y \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Install packages for python2/3 envs
RUN $PYTHON2_PATH/bin/pip install \
    jupyter-client==5.3.4 \
    numpy==1.16.4 \
    bohrium \
    scipy \
    h5py \
    pandas \
    sklearn \
    seaborn \
    scikit-image \
    pillow \
    tqdm \
    netCDF4 \
    graphviz \
    torch \
    torchvision \
	&& $PYTHON3_PATH/bin/pip install \
	jupyter-client==5.3.4 \
    numpy==1.16.4 \
    bohrium \
    scipy \
    h5py \
    pandas \
    sklearn \
    seaborn \
    scikit-image \
    pillow \
    tqdm \
    netCDF4 \
    graphviz \
    torch \
    torchvision \
    && $ASTRA_PATH/bin/pip install \
    jupyter-client==5.3.4 \
    numpy==1.16.4 \
    bohrium \
    ipympl \
    ipyleaflet \
    matplotlib \
    scipy \
    h5py \
    pandas \
    sklearn \
    seaborn \
    scikit-image \
    pillow \
    tqdm \
    netCDF4 \
    graphviz \
    torch \
    torchvision \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Add astra python to local path
RUN ln -s $ASTRA_PATH/bin/python /home/$NB_USER/.local/bin/python_astra \
    && ln -s $ASTRA_PATH/bin/python /home/$NB_USER/.local/bin/python3_astra

WORKDIR /home/$NB_USER

# Ensure that container Runs as
USER $NB_UID
