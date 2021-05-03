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
ENV PYTHON3_PATH=$CONDA_DIR/envs/python3

# Create user python2/3 environement
COPY environment.yml /tmp/
RUN conda env create -n python3 -f environment.yml \
    && $PYTHON3_PATH/bin/python -m ipykernel install --user --name=python3 \
    && conda clean --all -f -y \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

COPY requirements.txt /tmp/
RUN conda run -n python3 pip install -r requirements.txt \
    && conda clean --all -f -y \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

USER root
WORKDIR /home/$NB_USER

# Ensure that container Runs as
USER $NB_UID
