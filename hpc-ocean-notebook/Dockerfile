FROM nielsbohr/slurm-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60

RUN $PYTHON2_PATH/bin/pip install \
    botorch \
    jax \
    jaxlib \
    bohrium \
    veros \
    tensorflow \
    && $PYTHON3_PATH/bin/pip install \
    botorch \
    jax \
    jaxlib \
    bohrium \
    veros \
    tensorflow \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Run container as
USER $NB_UID
