FROM nielsbohr/python-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60

USER root

# Setup default timeout of installing packages
RUN echo "[global]" > /etc/pip.conf \
    && echo "timeout=$PACKAGE_TIMEOUT" >> /etc/pip.conf

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    gnupg2 \
    screen \
    tmux \
    build-essential \
    gcc-6 \
    g++-6 \
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

# NVIDIA package repository
RUN apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub \
    && wget http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_9.1.85-1_amd64.deb \
    && apt install ./cuda-repo-ubuntu1604_9.1.85-1_amd64.deb \
    && wget http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/x86_64/nvidia-machine-learning-repo-ubuntu1604_1.0.0-1_amd64.deb \
    && apt install ./nvidia-machine-learning-repo-ubuntu1604_1.0.0-1_amd64.deb \
    && rm -r cuda-repo-ubuntu1604_9.1.85-1_amd64.deb \
    nvidia-machine-learning-repo-ubuntu1604_1.0.0-1_amd64.deb

# CUDA env
ENV CUDA_VERSION 9.0.176
ENV CUDA_PKG_VERSION 9-0=$CUDA_VERSION-1
RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-libraries-$CUDA_PKG_VERSION \
    cuda-cudart-$CUDA_PKG_VERSION \
    && ln -s cuda-9.0 /usr/local/cuda

ENV PATH /usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/cuda/lib64
ENV LIBRARY_PATH /usr/local/cuda/lib64

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV NVIDIA_REQUIRE_CUDA "cuda>=9.0"

# Install CUDA and TensorRT runtime
RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    cuda-command-line-tools-9-0 \
    cuda-cublas-9-0 \
    cuda-cufft-9-0 \
    cuda-curand-9-0 \
    cuda-cusolver-9-0 \
    cuda-cusparse-9-0 \
    libcudnn7=7.2.1.38-1+cuda9.0 \
    libnccl2=2.2.13-1+cuda9.0 \
    libfreetype6-dev \
    libhdf5-serial-dev \
    libzmq3-dev \
    pkg-config \
    software-properties-common \
    unzip \
    && apt-get update \
    && apt-get install -yq --no-install-recommends \
    nvinfer-runtime-trt-repo-ubuntu1604-4.0.1-ga-cuda9.0 \
    && apt-get update \
    && apt-get install libnvinfer4=4.1.2-1+cuda9.0 \
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
    tensorflow-gpu==1.12.0 \
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
    git+https://www.github.com/keras-team/keras-contrib.git@e1574a16f0156dd9557fe62a1c5a39e37bd656c6 \
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
    tensorflow-gpu==1.12.0 \
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
    git+https://www.github.com/keras-team/keras-contrib.git@e1574a16f0156dd9557fe62a1c5a39e37bd656c6 \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Matplotlib basemap
RUN $PYTHON2_PATH/bin/pip install git+https://github.com/matplotlib/basemap.git@00794384f59e235f1e2847f952fd08b0bdc4327f \
    && $PYTHON3_PATH/bin/pip install git+https://github.com/matplotlib/basemap.git@00794384f59e235f1e2847f952fd08b0bdc4327f

USER root

RUN ln -s /usr/bin/gcc-6 /usr/local/cuda/bin/gcc \
    && ln -s /usr/bin/g++-6 /usr/local/cuda/bin/g++

WORKDIR /home/$NB_USER

# Run container as
USER $NB_UID
