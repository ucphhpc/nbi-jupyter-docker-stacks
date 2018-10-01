FROM nielsbohr/python-notebook:latest
MAINTAINER Rasmus Munk <rasmus.munk@nbi.ku.dk>

USER root

RUN apt-get update && apt-get -yq dist-upgrade \
    && apt-get install -yq --no-install-recommends \
    gnupg2 \
    vim \
    nano \
    htop \
    screen \
    tmux \
    libx11-6 \
    libsm6 \
    libxext6 \
    libgeos-dev \
    libglib2.0-0 \
    libxrender1 \
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
    cuda-cudart-$CUDA_PKG_VERSION \
    && ln -s cuda-9.0 /usr/local/cuda

ENV PATH /usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/cuda/lib64

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV NVIDIA_REQUIRE_CUDA "cuda>=9.0"

# Install CUDA and TensorRT runtime
RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    build-essential \
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
    unzip

RUN apt-get update \
    && apt-get install nvinfer-runtime-trt-repo-ubuntu1604-4.0.1-ga-cuda9.0 \
    && apt-get update \
    && apt-get install libnvinfer4=4.1.2-1+cuda9.0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER $NB_USER

# Environment variables
ENV BH_CONFIG=$PYTHON2_PATH/lib/python2.7/site-packages/bohrium/config.ini

# Packages
RUN $PYTHON2_PATH/bin/pip install \
    numpy \
    bohrium \
    opencv-python \
    statsmodels \
    ruamel.yaml \
    nibabel \
    keras \
    tensorflow-gpu \
    && $PYTHON3_PATH/bin/pip install \
    numpy \
    bohrium \
    opencv-python \
    statsmodels \
    ruamel.yaml \
    nibabel \
    keras \
    tensorflow-gpu

# Run container as
USER $NB_USER

# Matplotlib basemap
RUN $PYTHON2_PATH/bin/pip install https://github.com/matplotlib/basemap/archive/v1.2.0rel.tar.gz \
    && $PYTHON3_PATH/bin/pip install https://github.com/matplotlib/basemap/archive/v1.2.0rel.tar.gz
