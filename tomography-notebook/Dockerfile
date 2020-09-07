FROM nielsbohr/python-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60

USER root

# Setup default timeout of installing packages
RUN echo "[global]" > /etc/pip.conf \
    && echo "timeout=$PACKAGE_TIMEOUT" >> /etc/pip.conf

# setup for installing netCDF4. possibly move to base-notebook if this is a common problem
RUN apt-get update \
    && apt-get install -y libhdf5-dev libnetcdf-dev \
    && ln -s /usr/include/hdf5/serial /usr/include/hdf5/include \
    && export HDF5_DIR=/usr/include/hdf5

WORKDIR /tmp

# Run container as
USER $NB_UID

RUN conda config --set remote_read_timeout_secs $PACKAGE_TIMEOUT

# Packages env
ENV BH_CONFIG=$PYTHON2_PATH/lib/python2.7/site-packages/bohrium_api/config.ini
ENV ASTRA_PATH=$CONDA_DIR/envs/astra

RUN conda create -n astra -c astra-toolbox/label/dev \
    astra-toolbox=1.9.0 \
    ipykernel \
    && $ASTRA_PATH/bin/python -m ipykernel install --user --name astra \
    && conda clean --all -f -y \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# bohrium_api needs to be present before bohrium install
# Numpy 1.17.* has dropped support of py2
RUN $PYTHON2_PATH/bin/pip install \
    numpy==1.16.4 \
    bohrium_api \
    pystan \
    pymc3==3.6 \
    && $PYTHON3_PATH/bin/pip install \
    bohrium_api \
    && $ASTRA_PATH/bin/pip install \
    bohrium_api \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Install packages for python2/3 envs
RUN $PYTHON2_PATH/bin/pip install \
    numpy==1.16.4 \
    bohrium \
    scipy \
    h5py \
    pandas \
    sklearn \
    seaborn \
    scikit-image \
    pillow==6.2.1 \
    tqdm \
    netCDF4 \
    graphviz==0.13.2 \
    torch \
    torchvision \
    future
RUN $PYTHON3_PATH/bin/pip install \
    numpy==1.16.4 \
    bohrium \
    scipy \
    h5py \
    pandas \
    sklearn \
    seaborn \
    scikit-image \
    pillow==6.2.1 \
    tqdm \
    netCDF4 \
    graphviz==0.13.2 \
    torch \
    torchvision \
    nbformat==5.0.7 \
    jupyter-client==6.1.5 \
    mig_meow \
    future
RUN $ASTRA_PATH/bin/pip install \
    numpy==1.16.4 \
    bohrium \
    ipympl \
    ipyleaflet \
    jupyter-client==6.1.5 \
    matplotlib \
    scipy \
    h5py \
    pandas \
    sklearn \
    seaborn \
    scikit-image \
    pillow==6.2.1 \
    tqdm \
    netCDF4 \
    graphviz==0.13.2 \
    torch \
    torchvision \
    nbformat==5.0.7 \
    mig_meow \
    future \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

RUN mkdir -p /home/$NB_USER/.local/bin/python_astra /home/$NB_USER/.local/bin/python3_astra
# Add astra python to local path
RUN ln -s $ASTRA_PATH/bin/python /home/$NB_USER/.local/bin/python_astra \
    && ln -s $ASTRA_PATH/bin/python /home/$NB_USER/.local/bin/python3_astra

WORKDIR /home/$NB_USER

# Ensure that container Runs as
USER $NB_UID

