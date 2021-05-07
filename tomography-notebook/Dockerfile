FROM nielsbohr/python-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60

USER root

# Setup default timeout of installing packages
RUN echo "[global]" > /etc/pip.conf \
    && echo "timeout=$PACKAGE_TIMEOUT" >> /etc/pip.conf

# setup for installing netCDF4. possibly move to base-notebook if this is a common problem
# RUN apt-get update \
#     && apt-get install -y libhdf5-dev libnetcdf-dev \
#     && ln -s /usr/include/hdf5/serial /usr/include/hdf5/include \
#     && export HDF5_DIR=/usr/include/hdf5

WORKDIR /tmp

# Run container as
USER $NB_UID

RUN conda config --set remote_read_timeout_secs $PACKAGE_TIMEOUT

# Packages env
# ENV ASTRA_PATH=$CONDA_DIR/envs/astra

# RUN conda create -n astra -c astra-toolbox/label/dev \
#     astra-toolbox=1.9.0 \
#     ipykernel \
#     && $ASTRA_PATH/bin/python -m ipykernel install --user --name astra \
#     && conda clean --all -f -y \
#     && fix-permissions $CONDA_DIR \
#     && fix-permissions /home/$NB_USER

# Install packages for python2/3 envs
# RUN conda run -n python3 pip install \
#     && fix-permissions $CONDA_DIR \
#     && fix-permissions /home/$NB_USER

COPY environment.yml /tmp/
RUN conda env update -n python3 -f environment.yml \
    && conda clean --all -f -y \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

COPY requirements.txt /tmp/
RUN conda run -n python3 pip install -r requirements.txt \
    && conda clean -y --all \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

WORKDIR /home/$NB_USER

# Ensure that container Runs as
USER $NB_UID

