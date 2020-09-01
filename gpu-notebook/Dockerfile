FROM nielsbohr/python-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60

USER root

# Setup default timeout of installing packages
RUN echo "[global]" > /etc/pip.conf \
    && echo "timeout=$PACKAGE_TIMEOUT" >> /etc/pip.conf

RUN apt-get update && apt-get install -yq --no-install-recommends \
    gnupg2 \
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
    libgl1-mesa-glx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

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
ENV NVIDIA_REQUIRE_CUDA "cuda>=10.2 brand=tesla,driver>=384,driver<385 brand=tesla,driver>=396,driver<397 brand=tesla,driver>=410,driver<411 brand=tesla,driver>=418,driver<419"
# NCCL
ENV NCCL_VERSION 2.5.6
ENV CUDNN_VERSION 7.6.5.32

# Install cuda 10.0 and 10.1 to begin with (default link)
RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-toolkit-10-0 \
    cuda-toolkit-10-1 \
    libcudnn7=$CUDNN_VERSION-1+cuda10.0 \
    libcudnn7-dev=$CUDNN_VERSION-1+cuda10.0 \
    libcudnn7=$CUDNN_VERSION-1+cuda10.1 \
    libcudnn7-dev=$CUDNN_VERSION-1+cuda10.1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install cuda 10.2
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

WORKDIR /tmp

USER $NB_UID

RUN conda config --set remote_read_timeout_secs $PACKAGE_TIMEOUT

# Packages env
ENV BH_CONFIG=$PYTHON2_PATH/lib/python2.7/site-packages/bohrium_api/config.ini

# bohrium_api needs to be present before bohrium install
RUN conda run -n python2 pip install \
    numpy==1.16.4 \
    bohrium_api \
    && conda run -n python3 pip install \
    bohrium_api \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Packages
# Ensure cpu only version of tensorflow is not included and add some
# additional requested packages
RUN conda run -n python2 pip install \
    bohrium \
    opencv-python==4.2.0.32 \
    statsmodels \
    ruamel.yaml \
    scikit-learn \
    nibabel \
    pandas \
    keras \
    scipy==1.2.2 \
    tensorflow \
    lightgbm \
    xgboost \
    # Last version to support python 2
    joblib==0.12.5 \
    pydot \
    graphviz \
    torch \
    # Last version to support python 2
    seaborn==0.9.1 \
    pillow==6.2.1 \
    torchvision \
    scikit-optimize \
    tqdm \
    # Last version to support python 2
    llvmlite==0.31.0 \
    # Last version to support python 2
    numba==0.47.0 \
    hdbscan \
    git+https://www.github.com/keras-team/keras-contrib.git@5ffab172661411218e517a50170bb97760ea567b \
    && conda run -n python3 pip install \
    scipy==1.4.1 \
    numpy==1.18.5 \
    bohrium \
    opencv-python \
    statsmodels \
    ruamel.yaml \
    scikit-learn==0.22.2.post1 \
    nibabel \
    pandas \
    keras \
    tensorflow-gpu \
    lightgbm \
    xgboost \
    joblib==0.13.2 \
    pydot \
    graphviz \
    torch \
    seaborn \
    pillow==6.2.1 \
    torchvision \
    scikit-optimize==0.7.4 \
    tqdm \
    numba \
    umap-learn \
    hdbscan \
    git+https://www.github.com/keras-team/keras-contrib.git@5ffab172661411218e517a50170bb97760ea567b \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

USER root

ENV CUDA_PATH="/usr/local/cuda"
ENV CUDA_10_0_PATH="/usr/local/cuda-10.0"
ENV CUDA_10_1_PATH="/usr/local/cuda-10.1"
ENV CUDA_10_2_PATH="/usr/local/cuda-10.2"

# Link against the most recent CUDA
RUN rm $CUDA_PATH && ln -s $CUDA_10_2_PATH $CUDA_PATH

USER $NB_UID

# CUDA libraries
ENV LD_LIBRARY_PATH $CUDA_PATH/lib64:$CUDA_10_1_PATH/lib64:$CUDA_10_0_PATH/lib64

WORKDIR /home/$NB_USER
# Run container as
USER $NB_UID

