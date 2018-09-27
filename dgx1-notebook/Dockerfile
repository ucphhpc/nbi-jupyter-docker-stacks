FROM nielsbohr/base-notebook:latest
MAINTAINER Rasmus Munk <rasmus.munk@nbi.ku.dk>

USER root

# Taken from
# https://gitlab.com/nvidia/cuda/blob/ubuntu18.04/10.0/base/Dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends
    gnupg2 \
    curl \
    ca-certificates \
    vi \
    vim \
    nano \
    htop \
    screen \
    tmux \
    && curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1704/x86_64/7fa2af80.pub | apt-key add - && \
    echo "deb http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1704/x86_64 /" > /etc/apt/sources.list.d/cuda.list && \
    apt-get purge --autoremove -y curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

ENV CUDA_VERSION 9.0.176

ENV CUDA_PKG_VERSION 9-0=$CUDA_VERSION-1
RUN apt-get update && apt-get install -y --no-install-recommends \
        cuda-cudart-$CUDA_PKG_VERSION && \
    ln -s cuda-9.0 /usr/local/cuda && \
    rm -rf /var/lib/apt/lists/*

# nvidia-docker 1.0
LABEL com.nvidia.volumes.needed="nvidia_driver"
LABEL com.nvidia.cuda.version="${CUDA_VERSION}"

RUN echo "/usr/local/nvidia/lib" >> /etc/ld.so.conf.d/nvidia.conf && \
    echo "/usr/local/nvidia/lib64" >> /etc/ld.so.conf.d/nvidia.conf

ENV PATH /usr/local/nvidia/bin:/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV NVIDIA_REQUIRE_CUDA "cuda>=9.0"
# Custom packages
RUN $PYTHON2_PATH/bin/pip install \
    nibabel \
    rumal-yaml \
    statsmodels \
    git+https://github.com/aleju/imgaug \
    opencv-python \
    tensorflow \
    keras \
    && $PYTHON3_PATH/bin/pip install \
    nibabel \
    rumal-yaml \
    statsmodels \
    git+https://github.com/aleju/imgaug \
    opencv-python \
    tensorflow \
    keras \
    && fix-permissions $CONDA_DIR

# Run container as
USER $NB_USER
