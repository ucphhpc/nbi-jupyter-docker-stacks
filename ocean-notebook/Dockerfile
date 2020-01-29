FROM nielsbohr/datascience-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60

RUN $PYTHON2_PATH/bin/pip install veros --user \
    && $PYTHON3_PATH/bin/pip install veros --user \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Run container as
USER $NB_UID
