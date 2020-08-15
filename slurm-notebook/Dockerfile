FROM nielsbohr/python-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"

ARG SLURM_VERSION=18.08.4
ARG SLURM_DOWNLOAD_MD5=75c76328159def203133505def7a99a6
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
    supervisor \
    munge \
    iputils-ping \
    libmunge-dev \
    libslurm-dev \
    libopenmpi2 \
    libopenmpi-dev \
    openmpi-bin \
    openmpi-common \
    libnss-ldap \
    libpam-ldap \
    python3-h5py \
    python3-h5py-dbg \
    python-h5py \
    python-h5py-dbg \
    ldap-utils \
    cgdb \
    csh \
    tcsh \
    autotools-dev \
    cmake-curses-gui \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

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

WORKDIR /tmp

USER $NB_UID

# Install slurm labextension
# jupyterlab_slurm does not support jlab > 2.0.0, wait for it
# to be updated before reintroduced
# RUN pip install jupyterlab_slurm \
#     && fix-permissions $CONDA_DIR \
#     && fix-permissions /home/$NB_USER

# RUN jupyter labextension install jupyterlab-slurm \
#     && npm cache clean --force \
#     && npm dedupe \
#     && rm -fr /home/$NB_USER/.yarn \
#     && rm -fr /home/$NB_USER/.npm \
#     && rm -rf /tmp/npm* \
#     && rm -fr /tmp/v8* \
#     && fix-permissions $CONDA_DIR \
#     && fix-permissions /home/$NB_USER

RUN conda config --set remote_read_timeout_secs $PACKAGE_TIMEOUT

# Add cling kernel
# https://github.com/QuantStack/xeus-cling
RUN conda create -n cling \
    && conda install xeus-cling -n cling -c conda-forge \
    && conda clean --all -f -y \
    && rm -fr /tmp/tmp* \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

ENV CXX_PATH=$CONDA_DIR/envs/cling
RUN cp -R $CXX_PATH/share/jupyter/kernels/* $CONDA_DIR/share/jupyter/kernels/

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
