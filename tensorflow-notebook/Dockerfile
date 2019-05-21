FROM nielsbohr/datascience-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"

# Run container as
USER $NB_UID

# Install packages for python2/3 envs
RUN $PYTHON2_PATH/bin/pip install \
    tensorflow \
    keras \
    && $PYTHON3_PATH/bin/pip install \
    tensorflow \
    keras

USER root

RUN fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Ensure that container Runs as
USER $NB_UID