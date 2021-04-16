FROM nielsbohr/python-notebook:edge
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60

USER root

WORKDIR /tmp

ARG CUDA_OS_DIST=ubuntu2004
ARG CUDA_CPU=x86_64
ARG CUDA_MAJOR_VERSION=11.0
ARG CUDA_MIN_VERSION=3
ENV CUDA_VERSION=${CUDA_MAJOR_VERSION}.${CUDA_MIN_VERSION}
ARG CUDA_PKG_VERSION=11-0

ARG NCCL_VERSION=2.9.6
ARG CUDNN_VERSION=8.1.1

RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 \
    ca-certificates \
    && curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/${CUDA_OS_DIST}/${CUDA_CPU}/7fa2af80.pub | apt-key add - \
    && echo "deb https://developer.download.nvidia.com/compute/cuda/repos/${CUDA_OS_DIST}/${CUDA_CPU} /" > /etc/apt/sources.list.d/cuda.list \
    && echo "deb https://developer.download.nvidia.com/compute/machine-learning/repos/${CUDA_OS_DIST}/${CUDA_CPU} /" > /etc/apt/sources.list.d/nvidia-ml.list \
    && apt-get purge --autoremove -y curl \
    && rm -rf /var/lib/apt/lists/*

# For libraries in the cuda-compat-* package: https://docs.nvidia.com/cuda/eula/index.html#attachment-a
RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-cudart-${CUDA_PKG_VERSION} \
    cuda-compat-${CUDA_PKG_VERSION} \
    cuda-libraries-${CUDA_PKG_VERSION} \
    cuda-libraries-dev-${CUDA_PKG_VERSION} \
    cuda-nvtx-${CUDA_PKG_VERSION} \
    cuda-nvml-dev-${CUDA_PKG_VERSION} \
    cuda-command-line-tools-${CUDA_PKG_VERSION} \
    cuda-minimal-build-${CUDA_PKG_VERSION} \
    libnccl2 \
    libcudnn8 \
    libcudnn8-dev \
    libnccl-dev \
    pkg-config \
    software-properties-common \
    unzip \
    && ln -s cuda-${CUDA_MAJOR_VERSION} /usr/local/cuda \
    && rm -rf /var/lib/apt/lists/*

ENV CUDA_PATH="/usr/local/cuda"
ENV CUDA_11_0_PATH="/usr/local/cuda-11.0"

ENV PATH="${CUDA_PATH}/bin:${PATH}"
ENV LD_LIBRARY_PATH="${CUDA_PATH}/lib64:${LD_LIBRARY_PATH}"

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility

# Install user packages
USER $NB_UID
WORKDIR /home/$NB_USER

RUN conda run -n python2 pip install \
    tensorflow \
    tensorflow-gpu \
    keras \
    && conda run -n python3 pip install \
    tensorflow \
    tensorflow-gpu \
    keras \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Ensure that container Runs as
USER $NB_UID
