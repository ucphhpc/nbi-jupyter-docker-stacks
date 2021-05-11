FROM nielsbohr/python-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60

USER root

WORKDIR /tmp

ARG CUDA_OS_DIST=ubuntu2004
ARG CUDA_CPU=x86_64
ARG CUDA_MAJOR_VERSION=11
ARG CUDA_MIN_VERSION=0
ENV CUDA_VERSION=${CUDA_MAJOR_VERSION}.${CUDA_MIN_VERSION}
ARG CUDA_PKG_VERSION=11-0

ARG NCCL_VERSION=2.9.6
ARG CUDNN_VERSION=8.1.1

ENV CUDA_PATH="/usr/local/cuda"
ENV CUDA_11_0_PATH="/usr/local/cuda-11.0"

RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 \
    ca-certificates \
    && curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/${CUDA_OS_DIST}/${CUDA_CPU}/7fa2af80.pub | apt-key add - \
    && echo "deb https://developer.download.nvidia.com/compute/cuda/repos/${CUDA_OS_DIST}/${CUDA_CPU} /" > /etc/apt/sources.list.d/cuda.list \
    && echo "deb https://developer.download.nvidia.com/compute/machine-learning/repos/${CUDA_OS_DIST}/${CUDA_CPU} /" > /etc/apt/sources.list.d/nvidia-ml.list \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# For libraries in the cuda-compat-* package: https://docs.nvidia.com/cuda/eula/index.html#attachment-a
RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-${CUDA_PKG_VERSION} \
    libnccl2 \
    libnccl-dev \
    libcudnn8 \
    libcudnn8-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add missing symlink for libcusolver
WORKDIR ${CUDA_PATH}/lib64
RUN ln -s libcusolver.so.11 libcusolver.so.10
WORKDIR /tmp

ENV PATH="${CUDA_PATH}/bin:${PATH}"
ENV LD_LIBRARY_PATH="${CUDA_PATH}/lib64:${LD_LIBRARY_PATH}"

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility

# set tensorflow verbosity to error level, (default is 0/everything)
ENV TF_CPP_MIN_LOG_LEVEL="3"

RUN chown $NB_UID:$NB_GID -R /tmp

# Install user packages
USER $NB_UID

COPY requirements.txt /tmp/
RUN conda run -n python3 pip install -r requirements.txt \
    && conda clean --all -f -y \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

WORKDIR /home/$NB_USER

# Ensure that container Runs as
USER $NB_UID
