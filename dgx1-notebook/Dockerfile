FROM nielsbohr/python-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60

USER root

# Setup default timeout of installing packages
RUN echo "[global]" > /etc/pip.conf \
    && echo "timeout=$PACKAGE_TIMEOUT" >> /etc/pip.conf

RUN apt-get update && apt-get install -yq --no-install-recommends \
    gnupg2 \
    screen \
    tmux \
    build-essential \
    libboost-python-dev \
    libboost-thread-dev \
    libx11-6 \
    libsm6 \
    libxext6 \
    libgeos-dev \
    libglib2.0-0 \
    libxrender1 \
    dvipng \
    graphviz \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/ubuntu18.04/10.0/base/Dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 ca-certificates \
    && curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub | apt-key add - \
    && echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64 /" > /etc/apt/sources.list.d/cuda.list \
    && echo "deb https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64 /" > /etc/apt/sources.list.d/nvidia-ml.list \
    && rm -rf /var/lib/apt/lists/*

ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64
ENV CUDA_VERSION 10.0.130
ENV CUDA_PKG_VERSION 10-0=$CUDA_VERSION-1
# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV NVIDIA_REQUIRE_CUDA "cuda>=10.0 brand=tesla,driver>=384,driver<385 brand=tesla,driver>=410,driver<411"
# NCCL
ENV NCCL_VERSION 2.4.8
ENV CUDNN_VERSION 7.6.4.38

# For libraries in the cuda-compat-* package: https://docs.nvidia.com/cuda/eula/index.html#attachment-a
RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-cudart-$CUDA_PKG_VERSION \
    cuda-compat-10-0 \
    cuda-libraries-$CUDA_PKG_VERSION \
    cuda-libraries-dev-$CUDA_PKG_VERSION \
    cuda-nvtx-$CUDA_PKG_VERSION \
    libnccl2=$NCCL_VERSION-1+cuda10.0 \
    libcudnn7=$CUDNN_VERSION-1+cuda10.0 \
    libcudnn7-dev=$CUDNN_VERSION-1+cuda10.0 \
    cuda-nvml-dev-$CUDA_PKG_VERSION \
    cuda-command-line-tools-$CUDA_PKG_VERSION \
    cuda-minimal-build-$CUDA_PKG_VERSION \
    libnccl-dev=$NCCL_VERSION-1+cuda10.0 \
    libfreetype6-dev \
    libhdf5-serial-dev \
    libzmq3-dev \
    pkg-config \
    software-properties-common \
    unzip \
    && apt-mark hold libnccl2 libcudnn7 \
    && ln -s cuda-10.0 /usr/local/cuda \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp

USER $NB_UID

RUN conda config --set remote_read_timeout_secs $PACKAGE_TIMEOUT

# Packages env
ENV BH_CONFIG=$PYTHON2_PATH/lib/python2.7/site-packages/bohrium_api/config.ini

# bohrium_api needs to be present before bohrium install
RUN $PYTHON2_PATH/bin/pip install \
    numpy==1.16.4 \
    bohrium_api \
    && $PYTHON3_PATH/bin/pip install \
    bohrium_api \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Packages
# Ensure cpu only version of tensorflow is not included and add some
# additional requested packages
RUN $PYTHON2_PATH/bin/pip install \
    bohrium \
    opencv-python \
    statsmodels \
    ruamel.yaml \
    sklearn \
    nibabel \
    pandas \
    keras \
    tensorflow-gpu \
    lightgbm \
    xgboost \
    joblib \
    pydot \
    graphviz \
    torch \
    seaborn \
    torchvision \
    scikit-optimize \
    tqdm \
    numba \
    umap-learn \
    hdbscan \
    git+https://www.github.com/keras-team/keras-contrib.git@5ffab172661411218e517a50170bb97760ea567b \
    && $PYTHON3_PATH/bin/pip install \
    numpy \
    bohrium \
    opencv-python \
    statsmodels \
    ruamel.yaml \
    sklearn \
    nibabel \
    pandas \
    keras \
    tensorflow-gpu \
    lightgbm \
    xgboost \
    joblib \
    pydot \
    graphviz \
    torch \
    seaborn \
    torchvision \
    scikit-optimize \
    tqdm \
    numba \
    umap-learn \
    hdbscan \
    git+https://www.github.com/keras-team/keras-contrib.git@5ffab172661411218e517a50170bb97760ea567b \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Matplotlib basemap
RUN $PYTHON2_PATH/bin/pip install git+https://github.com/matplotlib/basemap.git@00794384f59e235f1e2847f952fd08b0bdc4327f \
    && $PYTHON3_PATH/bin/pip install git+https://github.com/matplotlib/basemap.git@00794384f59e235f1e2847f952fd08b0bdc4327f

WORKDIR /home/$NB_USER
# Run container as
USER $NB_UID
