FROM nielsbohr/datascience-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"

# Run container as
USER $NB_USER

# Install packages for python2/3 envs
RUN $PYTHON2_PATH/bin/pip install \
    tensorflow \
    keras \
    && $PYTHON3_PATH/bin/pip install \
    tensorflow \
    keras \
    && fix-permissions $CONDA_DIR
