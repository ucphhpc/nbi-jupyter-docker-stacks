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

# TODO, don't remove curl
# https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/ubuntu18.04/10.1/base/Dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
	gnupg2 curl ca-certificates && \
    curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub | apt-key add - && \
    echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64 /" > /etc/apt/sources.list.d/cuda.list && \
    echo "deb https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64 /" > /etc/apt/sources.list.d/nvidia-ml.list && \
    apt-get purge --autoremove -y curl && \
    rm -rf /var/lib/apt/lists/*

ENV PATH /usr/local/nvidia/bin:/usr/local/cuda/bin:${PATH}
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


# NVIDIA package repository
#RUN apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub \
##    && wget http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_9.1.85-1_amd64.deb \
 #   && apt install ./cuda-repo-ubuntu1604_9.1.85-1_amd64.deb \
 #   && wget http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/x86_64/nvidia-machine-learning-repo-ubuntu1604_1.0.0-1_amd64.deb \
 #   && apt install ./nvidia-machine-learning-repo-ubuntu1604_1.0.0-1_amd64.deb \
 #   && rm -r cuda-repo-ubuntu1604_9.1.85-1_amd64.deb \
 #   nvidia-machine-learning-repo-ubuntu1604_1.0.0-1_amd64.deb


# For libraries in the cuda-compat-* package: https://docs.nvidia.com/cuda/eula/index.html#attachment-a
RUN apt-get update && apt-get install -y --no-install-recommends \
        cuda-cudart-$CUDA_PKG_VERSION \
        cuda-compat-10-0 \
        cuda-libraries-$CUDA_PKG_VERSION \
        cuda-nvtx-$CUDA_PKG_VERSION \
	    libnccl2=$NCCL_VERSION-1+cuda10.0 \
	    libcudnn7=$CUDNN_VERSION-1+cuda10.0 \
	    && apt-mark hold libnccl2 libcudnn7 && \
		ln -s cuda-10.0 /usr/local/cuda && \
    	rm -rf /var/lib/apt/lists/*

# CUDA envd
#ENV CUDA_VERSION 9.0.176
#ENV CUDA_PKG_VERSION 9-0=$CUDA_VERSION-1
#RUN apt-get update && apt-get install -y --no-install-recommends \
#    cuda-libraries-$CUDA_PKG_VERSION \
#    cuda-cudart-$CUDA_PKG_VERSION \
#    && ln -s cuda-9.0 /usr/local/cuda
#
#    cuda-command-line-tools-9-0 \
#    cuda-cublas-9-0 \
#    cuda-cufft-9-0 \
#    cuda-curand-9-0 \
#    cuda-cusolver-9-0 \
#    cuda-cusparse-9-0 \
#    libcudnn7=7.2.1.38-1+cuda9.0 \
#    libnccl2=2.2.13-1+cuda9.0 \

#&& apt-get update \
#    && apt-get install -yq --no-install-recommends \
#    nvinfer-runtime-trt-repo-ubuntu1604-4.0.1-ga-cuda9.0 \
#    && apt-get update \
#    && apt-get install libnvinfer4=4.1.2-1+cuda9.0 \

# Install CUDA and TensorRT runtime
RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    libfreetype6-dev \
    libhdf5-serial-dev \
    libzmq3-dev \
    pkg-config \
    software-properties-common \
    unzip \
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

USER root

#RUN ln -s /usr/bin/gcc-6 /usr/local/cuda/bin/gcc \
#    && ln -s /usr/bin/g++-6 /usr/local/cuda/bin/g++

WORKDIR /home/$NB_USER

# Run container as
USER $NB_UID
