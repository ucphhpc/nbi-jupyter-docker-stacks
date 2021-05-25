FROM nielsbohr/python-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60

USER root

# Setup default timeout of installing packages
RUN echo "[global]" > /etc/pip.conf \
    && echo "timeout=$PACKAGE_TIMEOUT" >> /etc/pip.conf

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    pkg-config \
    gmsh \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -fr /tmp/tmp*

WORKDIR /tmp
USER $NB_UID

ENV PKG_CONFIG_PATH=$PYTHON3_PATH/lib/pkgconfig

RUN conda config --set remote_read_timeout_secs $PACKAGE_TIMEOUT

COPY environment.yml /tmp/
RUN conda env update -n python3 -f environment.yml \
    && conda clean --all -f -y \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

COPY requirements.txt /tmp/
RUN conda run -n python3 pip install -r requirements.txt \
    && conda clean --all -f -y \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Ensure that the pkg config can be found in Jupyter
RUN conda run -n python3 python3 /usr/local/bin/update_kernel_spec.py python3 --env-kwargs PATH=$PYTHON3_PATH/bin:$PATH

WORKDIR /home/$NB_USER

# Ensure that container Runs as
USER $NB_UID