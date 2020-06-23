FROM nielsbohr/slurm-notebook:latest
LABEL MAINTAINER="Mads R. B. Kristensen <madsbk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60
ARG BOHRIUM_VERSION=0.11.0

USER root

# Setup default timeout of installing packages
RUN echo "[global]" > /etc/pip.conf \
    && echo "timeout=$PACKAGE_TIMEOUT" >> /etc/pip.conf

# Dep
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    cmake \
    gfortran \
    libboost-filesystem-dev \
    libboost-serialization-dev \
    libboost-regex-dev \
    libboost-program-options-dev \
    zlib1g-dev \
    libsigsegv-dev \
    freeglut3 \
    freeglut3-dev \
    libxmu-dev \
    libxi-dev \
    libhdf5-dev \
    libhdf5-doc \
    xtensor-dev \
    xtensor-doc \
    libjson-c-dev \
    libnetcdf-dev \
    libnetcdff-dev \
    libnetcdff-doc \
    python3-h5py \
    python3-h5py-dbg \
    python-h5py \
    python-h5py-dbg \
    cgdb \
    csh \
    tcsh \
    autotools-dev \
    autoconf \
    cmake-curses-gui \
    automake \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp

RUN curl -LOk https://github.com/bh107/bohrium/archive/v${BOHRIUM_VERSION}.tar.gz \
    && tar -xf v${BOHRIUM_VERSION}.tar.gz \
    && mkdir bohrium-${BOHRIUM_VERSION}/build \
    && cd bohrium-${BOHRIUM_VERSION}/build \
    && cmake .. -DVE_OPENCL=OFF -DVE_CUDA=OFF -DEXT_CLBLAS=OFF -DBRIDGE_PY_API=OFF -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=/usr \
    && make install -j 2 \
    && cd /tmp \
    && rm -r bohrium-${BOHRIUM_VERSION} \
    && mkdir -p /usr/var/bohrium \
    && chmod 777 /usr/var/bohrium

RUN mkdir -p /opt \
    && chgrp $NB_GID /opt \
    && chmod 774 /opt

# Launch script
RUN echo "#!/usr/bin/env bash" > /usr/local/bin/hpc_launch.sh && \
    echo "set -e" >> /usr/local/bin/hpc_launch.sh && \
    echo "git clone https://github.com/ucphhpc/hpc_course.git /opt/hpc_course" >> /usr/local/bin/hpc_launch.sh && \
    echo "chgrp -R $NB_GID /opt/hpc_course" >> /usr/local/bin/hpc_launch.sh && \
    echo "chmod -R g+w /opt/hpc_course" >> /usr/local/bin/hpc_launch.sh
RUN chmod a+x /usr/local/bin/hpc_launch.sh

COPY supervisord.conf /etc/supervisor/hpc-supervisord.conf
RUN cat /etc/supervisor/hpc-supervisord.conf >> /etc/supervisor/supervisord.conf \
    && rm -fr /etc/supervisor/hpc-supervisord.conf

USER $NB_UID

RUN conda config --set remote_read_timeout_secs $PACKAGE_TIMEOUT

RUN conda install --quiet --yes \
    ffmpeg \
    imagemagick \
    && conda clean --all -f -y \
    && rm -fr /tmp/tmp* \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

RUN pip install h5py

WORKDIR /home/$NB_USER

# Install code-server (https://github.com/betatim/vscode-binder/blob/master/postBuild)
ARG CODE_SERVER_VERSION="2.1698"
ARG CODE_SERVER_VSC_VERSION="vsc1.41.1"
# Download and install VS Code server
RUN wget -q -O code-server.tar.gz https://github.com/cdr/code-server/releases/download/${CODE_SERVER_VERSION}/code-server${CODE_SERVER_VERSION}-${CODE_SERVER_VSC_VERSION}-linux-x86_64.tar.gz \
	&& mkdir -p ~/.local/bin \
	&& tar -xvf code-server.tar.gz -C ~/.local/bin --strip-components=1 \
	&& rm -rf code-server.tar.gz

# Python extension
RUN wget https://github.com/microsoft/vscode-python/releases/download/2019.10.44104/ms-python-release.vsix \
	&& $HOME/.local/bin/code-server --install-extension ms-python-release.vsix \
	&& rm -rf ms-python-release.vsix

ENV PATH="$PATH:$HOME/.local/bin"

# As an exception, run as root,
# Remember to use supervisord start-notebook.sh to
# de-escalate privileges to $NB_UID:$NB_GID
USER root
