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
RUN conda create -n python2 python=2.7 ipykernel \
    && conda create -n python3 python=3.7 ipykernel \
    && $PYTHON2_PATH/bin/python -m ipykernel install --user \
    && $PYTHON3_PATH/bin/python -m ipykernel install --user \
    && conda clean --all -f -y \
    && rm -fr /tmp/tmp*

# Ensure $NB_USER uses the conda python envs
RUN mkdir -p /home/$NB_USER/.local/bin

RUN ln -s $PYTHON2_PATH/bin/python /home/$NB_USER/.local/bin/python2 \
    && ln -s $PYTHON2_PATH/bin/python /home/$NB_USER/.local/bin/python2.7 \
    && ln -s $PYTHON2_PATH/bin/pip /home/$NB_USER/.local/bin/pip2 \
    && ln -s $PYTHON2_PATH/bin/pip /home/$NB_USER/.local/bin/pip2.7 \
    && ln -s $PYTHON3_PATH/bin/python /home/$NB_USER/.local/bin/python \
    && ln -s $PYTHON3_PATH/bin/python /home/$NB_USER/.local/bin/python3 \
    && ln -s $PYTHON3_PATH/bin/python /home/$NB_USER/.local/bin/python3.7 \
    && ln -s $PYTHON3_PATH/bin/python /home/$NB_USER/.local/bin/python3.7m \
    && ln -s $PYTHON3_PATH/bin/pip /home/$NB_USER/.local/bin/pip \
    && ln -s $PYTHON3_PATH/bin/pip /home/$NB_USER/.local/bin/pip3 \
    && ln -s $PYTHON3_PATH/bin/python3.7m-config /home/$NB_USER/.local/bin/python3.7-config \
    && ln -s $PYTHON3_PATH/bin/python3.7m-config /home/$NB_USER/.local/bin/python3.7m-config

# upgrade pip
# Add matplotlib widget for jlab
RUN $PYTHON2_PATH/bin/pip install \
    ipympl \
    ipyleaflet \
    matplotlib \
    && $PYTHON3_PATH/bin/pip install \
    ipympl \
    ipyleaflet \
    matplotlib

USER root

RUN echo "PATH=\"/home/$NB_USER/.local/bin:$PATH\"" >> /home/$NB_USER/.bashrc

RUN fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

WORKDIR /home/$NB_USER

# Ensure that container Runs as
USER $NB_UID
