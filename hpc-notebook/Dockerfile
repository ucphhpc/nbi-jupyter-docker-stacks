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
    && rm -r bohrium-${BOHRIUM_VERSION}

RUN mkdir -p /opt \
    && chgrp $NB_GID /opt \
    && chmod 774 /opt

# Launch script
RUN echo "#!/usr/bin/env bash" > /usr/local/bin/hpc_launch.sh && \
    echo "set -e" >> /usr/local/bin/hpc_launch.sh && \
    echo "git clone https://github.com/madsbk/hpc_course.git /opt/hpc_course" >> /usr/local/bin/hpc_launch.sh && \
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

# As an exception, run as root,
# Remember to use supervisord start-notebook.sh to
# de-escalate privileges to $NB_UID:$NB_GID
USER root
