FROM nielsbohr/python-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"

ARG SLURM_VERSION=21.08.0
ARG SLURM_DOWNLOAD_MD5=a5bf9ab2733f520cd8229513431ad787
ARG SLURM_DOWNLOAD_URL="https://download.schedmd.com/slurm/slurm-$SLURM_VERSION.tar.bz2"
ARG PACKAGE_TIMEOUT=60

USER root

# Setup default timeout of installing packages
RUN echo "[global]" > /etc/pip.conf \
    && echo "timeout=$PACKAGE_TIMEOUT" >> /etc/pip.conf

RUN groupadd -r slurm --gid=990 && useradd -r -g slurm --uid=990 slurm \
    && groupadd -r munge --gid=993 && useradd -r -g munge --uid=997 munge

# Dependencies
# build, slurm, openmpi, ldap
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    autotools-dev \
    cgdb \
    cmake-curses-gui \
    csh \
    g++ \
    g++-10 \
    g++-8 \
    g++-9 \
    gcc \
    gcc-10 \
    gcc-8 \
    gcc-9 \
    iputils-ping \
    ldap-utils \
    libhdf5-dev \
    libhdf5-doc \
    libmunge-dev \
    libnss-ldap \
    libopenmpi-dev \
    libpam-ldap \
    libslurm-dev \
    munge \
    openmpi-bin \
    python3-h5py \
    python3-h5py-dbg \
    supervisor \
    tcsh \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp

RUN cd \
    && wget -O slurm.tar.bz2 "$SLURM_DOWNLOAD_URL" \
    && echo "$SLURM_DOWNLOAD_MD5" slurm.tar.bz2 | md5sum -c - \
    && mkdir -p /usr/local/src/slurm \
    && tar jxf slurm.tar.bz2 -C /usr/local/src/slurm --strip-components=1 \
    && cd /usr/local/src/slurm \
    && ./configure --enable-debug --prefix=/usr --sysconfdir=/etc/slurm \
        --libdir=/usr/lib \
    && make install \
    && cd \
    && rm -f slurm.tar.bz2

# Required directories
RUN mkdir -p /var/run/munge \
    && chown -R munge:munge /var/run/munge \
    && chown -R munge:munge /var/log/munge \
    && chmod -R 770 /var/log/munge

RUN mkdir -p /var/spool/slurmd \
    && chown slurm:slurm /var/spool/slurmd \
    && chmod 775 /var/spool/slurmd

USER $NB_UID

RUN conda config --set remote_read_timeout_secs $PACKAGE_TIMEOUT
ENV CLING_PATH=$CONDA_DIR/envs/cling

# Install packages for python3 envs
COPY requirements.txt /tmp/
RUN conda run -n python3 pip install -r requirements.txt \
    && conda clean -y --all \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Add cling kernel
# https://github.com/QuantStack/xeus-cling
COPY environment.yml /tmp/
RUN conda env create -n cling -f environment.yml \
    && conda clean --all -f -y \
    && rm -fr /tmp/tmp* \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

ENV CXX_PATH=$CONDA_DIR/envs/cling
RUN cp -R $CXX_PATH/share/jupyter/kernels/* $CONDA_DIR/share/jupyter/kernels/

# Add the cling environment to the jupyter kernel path
RUN conda run -n cling python3 /usr/local/bin/update_kernel_spec.py cling --env-kwargs PATH=$CLING_PATH/bin:$PATH

# TODO, Add PySlurm (Python interface to slurm) requires Cython
# Requires slurm 19.05
USER root

# Prepare supervisord state dirs
RUN mkdir -p /var/log/supervisord /var/run/supervisord \
    && chown $NB_UID:$NB_GID /var/log/supervisord \
    && chown $NB_UID:$NB_GID /var/run/supervisord \
    && chmod 775 /var/log/supervisord \
    && chmod 775 /var/run/supervisord

COPY supervisord.conf /etc/supervisor/supervisord.conf
RUN chown $NB_UID:$NB_GID /etc/supervisor/supervisord.conf \
    && chmod 775 /etc/supervisor/supervisord.conf

WORKDIR /home/$NB_USER

USER root
# As an exception, run as root,
# Remember to use supervisord start-notebook.sh to
# de-escalate privileges to $NB_UID:$NB_GID
CMD ["/usr/bin/supervisord"]
