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

# NCCL
ENV NCCL_VERSION 2.5.6
ENV CUDNN_VERSION 7.6.5.32

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-toolkit-10-0 \
    cuda-toolkit-10-1 \
    libcudnn7=$CUDNN_VERSION-1+cuda10.0 \
    libcudnn7-dev=$CUDNN_VERSION-1+cuda10.0 \
    libcudnn7=$CUDNN_VERSION-1+cuda10.1 \
    libcudnn7-dev=$CUDNN_VERSION-1+cuda10.1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install cuda 10.0 and 10.1 to begin with (default link)
# Then install cuda 10.2
# For libraries in the cuda-compat-* package: https://docs.nvidia.com/cuda/eula/index.html#attachment-a
RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-cudart-$CUDA_PKG_VERSION \
    cuda-compat-10-2 \
    cuda-libraries-$CUDA_PKG_VERSION \
    cuda-libraries-dev-$CUDA_PKG_VERSION \
    cuda-nvtx-$CUDA_PKG_VERSION \
    libnccl2=$NCCL_VERSION-1+cuda10.2 \
    libcudnn7=$CUDNN_VERSION-1+cuda10.2 \
    libcudnn7-dev=$CUDNN_VERSION-1+cuda10.2 \
    cuda-nvml-dev-$CUDA_PKG_VERSION \
    cuda-command-line-tools-$CUDA_PKG_VERSION \
    cuda-minimal-build-$CUDA_PKG_VERSION \
    libnccl-dev=$NCCL_VERSION-1+cuda10.2 \
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

RUN conda run -n python2 pip install \
    scipy==1.2.2 \
    jax \
    jaxlib \
    bohrium \
    veros \
    xarray \
    netCDF4 \
    tensorflow \
    && conda run -n python3 pip install \
    numpy==1.18.4 \
    scipy==1.4.1 \
    botorch \
    jax \
    jaxlib \
    bohrium \
    veros \
    xarray \
    netCDF4 \
    tensorflow \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Tensorflow still looks for cuda-10.1
# 10.2 is backward comptable so we just create the link targets to them
# ENV CUDA_LEGACY_PATH="/usr/local/cuda-10.1"
# ENV CUDA_LEGACY_LIB_PATH="$CUDA_LEGACY_PATH/lib64"

RUN apt-get install -y --no-install-recommends \
    cuda-toolkit-10-0 \
    cuda-toolkit-10-1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


USER $NB_UID

# CUDA libraries
ENV LD_LIBRARY_PATH $CUDA_LEGACY_LIB_PATH:/usr/local/cuda/lib64:/usr/local/cuda-10.0/extras/CUPTI/lib64

WORKDIR /home/$NB_USER
# As an exception, run as root,
# Remember to use supervisord start-notebook.sh to
# de-escalate privileges to $NB_UID:$NB_GID
USER root
