FROM nielsbohr/python-notebook:edge

USER root

# For opencv2 and basemap geos
RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    libx11-6 \
    libsm6 \
    libxext6 \
    libgeos-dev \
    libglib2.0-0 \
    libxrender1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Run container as
USER $NB_USER

# Install packages for python2/3 envs
RUN $PYTHON2_PATH/bin/pip install \
    numpy \
    bohrium \
    opencv-python \
    scipy \
    pandas \
    sklearn \
    seaborn \
    scikit-image \
    pillow \
    && $PYTHON3_PATH/bin/pip install \
    numpy \
    bohrium \
    opencv-python \
    scipy \
    pandas \
    sklearn \
    seaborn \
    scikit-image \
    pillow \
    && fix-permissions $CONDA_DIR

# Environment variables
ENV BH_CONFIG=$PYTHON2_PATH/lib/python2.7/site-packages/bohrium/config.ini

# Matplotlib basemap
RUN $PYTHON2_PATH/bin/pip install https://github.com/matplotlib/basemap/archive/v1.2.0rel.tar.gz \
    && $PYTHON3_PATH/bin/pip install https://github.com/matplotlib/basemap/archive/v1.2.0rel.tar.gz
