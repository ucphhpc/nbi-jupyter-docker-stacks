FROM nielsbohr/base-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"

ARG SLURM_VERSION=18.08.4
ARG SLURM_DOWNLOAD_MD5=75c76328159def203133505def7a99a6
ARG SLURM_DOWNLOAD_URL="https://download.schedmd.com/slurm/slurm-$SLURM_VERSION.tar.bz2"

USER root

RUN groupadd -r slurm --gid=990 && useradd -r -g slurm --uid=990 slurm \
    && groupadd -r munge --gid=993 && useradd -r -g munge --uid=997 munge

# Dep
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    supervisor \
    make \
    cmake \
    munge \
    iputils-ping \
    libmunge-dev \
    libslurm-dev \
    libopenmpi2 \
    libopenmpi-dev \
    openmpi-bin \
    openmpi-common \
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

USER $NB_USER

# Add cling kernel
# https://github.com/QuantStack/xeus-cling
RUN conda create -n cling \
    && conda install xeus-cling -n cling -c conda-forge \
    && conda clean -tipsy \
    && fix-permissions $CONDA_DIR

ENV CXX_PATH=$CONDA_DIR/envs/cling
RUN cp -R $CXX_PATH/share/jupyter/kernels/* $CONDA_DIR/share/jupyter/kernels/

USER root

# Prepare supervisord state dirs
RUN mkdir -p /var/log/supervisord /var/run/supervisord \
    && chown $NB_USER:$NB_GID /var/log/supervisord \
    && chown $NB_USER:$NB_GID /var/run/supervisord \
    && chmod 775 /var/log/supervisord \
    && chmod 775 /var/run/supervisord

COPY supervisord.conf /etc/supervisor/supervisord.conf
COPY setup_env.sh /usr/local/bin/setup_env.sh
RUN chown $NB_USER:$NB_GID /etc/supervisor/supervisord.conf \
    && chmod 775 /etc/supervisor/supervisord.conf \
    && chown $NB_USER:$NB_GID /usr/local/bin/setup_env.sh \
    && chmod +x /usr/local/bin/setup_env.sh

CMD ["/usr/bin/supervisord"]
