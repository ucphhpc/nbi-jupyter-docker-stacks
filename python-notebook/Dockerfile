FROM nielsbohr/base-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60

USER root

# Setup default timeout of installing packages
RUN echo "[global]" > /etc/pip.conf \
    && echo "timeout=$PACKAGE_TIMEOUT" >> /etc/pip.conf

WORKDIR /tmp

USER $NB_UID

RUN conda config --set remote_read_timeout_secs $PACKAGE_TIMEOUT

ENV PYTHON2_PATH=$CONDA_DIR/envs/python2
ENV PYTHON3_PATH=$CONDA_DIR/envs/python3

# Create user python2/3 environement
RUN conda create -n python2 python=2.7 ipykernel backports.functools_lru_cache \
    && conda create -n python3 python=3.7 ipykernel \
    && $PYTHON2_PATH/bin/python -m ipykernel install --user \
    && $PYTHON3_PATH/bin/python -m ipykernel install --user \
    && conda clean --all -f -y \
    && rm -fr /tmp/tmp* \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# upgrade pip
# Add matplotlib widget for jlab
RUN conda run -n python2 pip install \
    ipympl \
    ipyleaflet \
    matplotlib \
    jupyter-client==5.3.4 \
    && conda run -n python3 pip install \
    ipympl \
    ipyleaflet \
    matplotlib \
    jupyter-client==5.3.4 \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

USER root
WORKDIR /home/$NB_USER

# Ensure that container Runs as
USER $NB_UID
