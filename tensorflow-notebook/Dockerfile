FROM nielsbohr/datascience-notebook:latest
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

# Install packages for python2/3 envs
RUN $PYTHON2_PATH/bin/pip install \
    future \
    pillow==6.2.1 \
    tensorflow \
    keras \
    torch \
    torchvision \
    lightgbm \
    && $PYTHON3_PATH/bin/pip install \
    pillow==6.2.1 \
    tensorflow \
    keras \
    torch \
    torchvision \
    lightgbm \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

WORKDIR /home/$NB_USER

# Ensure that container Runs as
USER $NB_UID
