FROM nielsbohr/python-notebook:latest
MAINTAINER Rasmus Munk <rasmus.munk@nbi.ku.dk>

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

# Packages env
ENV BH_CONFIG=$PYTHON2_PATH/lib/python2.7/site-packages/bohrium_api/config.ini

# Install packages for python2/3 envs
RUN $PYTHON2_PATH/bin/pip install \
    numpy \
    bohrium==0.10.0.post19 \
    cython \
    pandas \
    opencv-python \
    six \
    nose \
    scipy \
    sympy \
    h5py \
    pandas \
    sklearn \
    seaborn \
    scikit-image \
    pillow \
    && $PYTHON3_PATH/bin/pip install \
    numpy \
    bohrium==0.10.0.post19 \
    cython \
    pandas \
    opencv-python \
    six \
    nose \
    sympy \
    scipy \
    h5py \
    pandas \
    sklearn \
    seaborn \
    scikit-image \
    pillow \
    && fix-permissions $CONDA_DIR

# Matplotlib basemap
RUN $PYTHON2_PATH/bin/pip install git+https://github.com/matplotlib/basemap.git \
    && $PYTHON3_PATH/bin/pip install git+https://github.com/matplotlib/basemap.git

# Install diffpy
ENV PYTHON2_DIFFPY_PATH=$CONDA_DIR/envs/python2_diffpy

RUN conda create -n python2_diffpy python=2.7 ipykernel \
    && conda config --add channels diffpy \
    && conda install -n python2_diffpy diffpy-cmi \
    && conda clean -tipsy \
    && fix-permissions $CONDA_DIR \
    && sed -i 's/"Python 2"/"Python 2 diffpy-cmi"/g' $PYTHON2_DIFFPY_PATH/share/jupyter/kernels/python2/kernel.json \
    && mv $PYTHON2_DIFFPY_PATH/share/jupyter/kernels/python2 $PYTHON2_DIFFPY_PATH/share/jupyter/kernels/python2_diffpy \
    && cp -r $PYTHON2_DIFFPY_PATH/share/jupyter/kernels/python2_diffpy /home/$NB_USER/.local/share/jupyter/kernels/

RUN $PYTHON2_DIFFPY_PATH/bin/pip install \
    ase \
    && fix-permissions $CONDA_DIR
