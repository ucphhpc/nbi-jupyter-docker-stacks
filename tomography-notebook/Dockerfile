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

RUN conda create -n astra -c astra-toolbox \
    astra-toolbox \
    ipykernel \
    && $ASTRA_PATH/bin/python -m ipykernel install --user --name astra \
    && conda clean --all -f -y \
    && rm -fr /tmp/tmp*

# bohrium_api needs to be present before bohrium install
# Numpy 1.17.* has dropped support of py2
RUN $PYTHON2_PATH/bin/pip install \
    numpy==1.16.4 \
    bohrium_api \
    && $PYTHON3_PATH/bin/pip install \
    bohrium_api \
    && $ASTRA_PATH/bin/pip install \
    bohrium_api

# Install packages for python2/3 envs
RUN $PYTHON2_PATH/bin/pip install \
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
    && $PYTHON3_PATH/bin/pip install \
    numpy \
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
    && $ASTRA_PATH/bin/pip install \
    ipympl \
    ipyleaflet \
    matplotlib \
    numpy \
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
    graphviz

# Add astra python to local path
RUN ln -s $ASTRA_PATH/bin/python /home/$NB_USER/.local/bin/python_astra \
    && ln -s $ASTRA_PATH/bin/python /home/$NB_USER/.local/bin/python3_astra

USER root

RUN fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

WORKDIR /home/$NB_USER

# Ensure that container Runs as
USER $NB_UID
