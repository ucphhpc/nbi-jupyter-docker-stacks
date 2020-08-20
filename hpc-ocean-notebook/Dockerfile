FROM nielsbohr/slurm-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    libnetcdf-dev \
    libnetcdff-dev \
    libnetcdff-doc \
    libnetcdf-dev \
    libhdf5-dev \
    && apt-get clean \
    && rm -fr /var/lib/apt/lists/*

# Fix hdf5 link
RUN ln -s /usr/include/hdf5/serial /usr/include/hdf5/include

ENV HDF5_DIR="/usr/include/hdf5"

# Install CUDA
# https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/ubuntu18.04/10.0/base/Dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 ca-certificates \
    && curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub | apt-key add - \
    && echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64 /" > /etc/apt/sources.list.d/cuda.list \
    && echo "deb https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64 /" > /etc/apt/sources.list.d/nvidia-ml.list \
    && rm -rf /var/lib/apt/lists/*

ENV CUDA_VERSION 10.2.89
ENV CUDA_PKG_VERSION 10-2=$CUDA_VERSION-1
# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV NVIDIA_REQUIRE_CUDA "cuda>=10.2,driver>=384,driver<385,driver>=396,driver<397,driver>=410,driver<411,driver>=418,driver<419"
# NCCL
ENV NCCL_VERSION 2.5.6
ENV CUDNN_VERSION 7.6.5.32

# For libraries in the cuda-compat-* package: https://docs.nvidia.com/cuda/eula/index.html#attachment-a
RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-cudart-$CUDA_PKG_VERSION \
    cuda-compat-10-2 \
    cuda-libraries-$CUDA_PKG_VERSION \
    cuda-libraries-dev-$CUDA_PKG_VERSION \
    cuda-nvtx-$CUDA_PKG_VERSION \
    libcublas10=10.2.2.89-1 \
    libnccl2=$NCCL_VERSION-1+cuda10.2 \
    libcudnn7=$CUDNN_VERSION-1+cuda10.2 \
    libcudnn7-dev=$CUDNN_VERSION-1+cuda10.2 \
    cuda-nvml-dev-$CUDA_PKG_VERSION \
    cuda-command-line-tools-$CUDA_PKG_VERSION \
    cuda-minimal-build-$CUDA_PKG_VERSION \
    libnccl-dev=$NCCL_VERSION-1+cuda10.2 \
    libcublas-dev=10.2.2.89-1 \
    libfreetype6-dev \
    libhdf5-serial-dev \
    libzmq3-dev \
    pkg-config \
    software-properties-common \
    unzip \
    && apt-mark hold libnccl2 libcudnn7 \
    && ln -s cuda-10.2 /usr/local/cuda \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN $PYTHON2_PATH/bin/pip install \
    scipy==1.2.2 \
    jax \
    jaxlib \
    bohrium \
    veros \
    tensorflow \
    && $PYTHON3_PATH/bin/pip install \
    numpy==1.18.4 \
    scipy==1.4.1 \
    botorch \
    jax \
    jaxlib \
    bohrium \
    veros \
    tensorflow \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Tensorflow still looks for cuda-10.1
# 10.2 is backward comptable so we just create the link targets to them
ENV CUDA_LEGACY_PATH="/usr/local/cuda-10.1"
ENV CUDA_LEGACY_LIB_PATH="$CUDA_LEGACY_PATH/lib64"

USER root
RUN mkdir -p $CUDA_LEGACY_LIB_PATH \
    && ln -s /usr/local/cuda/lib64/libcudart.so $CUDA_LEGACY_LIB_PATH/libcudart.so.10.1 \
    && ln -s /usr/local/cuda/lib64/libcublas.so $CUDA_LEGACY_LIB_PATH/libcublas.so.10 \
    && ln -s /usr/local/cuda/lib64/libcufft.so $CUDA_LEGACY_LIB_PATH/libcufft.so.10 \
    && ln -s /usr/local/cuda/lib64/libcurand.so $CUDA_LEGACY_LIB_PATH/libcurand.so.10 \
    && ln -s /usr/local/cuda/lib64/libcurand.so $CUDA_LEGACY_LIB_PATH/libcusolver.so.10 \
    && ln -s /usr/local/cuda/lib64/libcusparse.so $CUDA_LEGACY_LIB_PATH/libcusparse.so.10 \
    && ln -s /usr/local/cuda-10.2/compat/libcuda.so.1 $CUDA_LEGACY_LIB_PATH/libcuda.so.1

USER $NB_UID

# CUDA libraries
ENV LD_LIBRARY_PATH $CUDA_LEGACY_LIB_PATH:/usr/local/cuda/lib64:/usr/local/cuda-10.0/extras/CUPTI/lib64

# Run container as
USER $NB_UID
