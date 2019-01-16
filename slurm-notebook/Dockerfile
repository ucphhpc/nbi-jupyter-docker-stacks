FROM nielsbohr/base-notebook:latest
MAINTAINER Rasmus Munk <rasmus.munk@nbi.ku.dk>

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
    make \
    munge \
    libmunge2 \
    libslurm-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN cd \
    && wget -O slurm.tar.bz2 "$SLURM_DOWNLOAD_URL" \
    && echo "$SLURM_DOWNLOAD_MD5" slurm.tar.bz2 | md5sum -c - \
    && mkdir -p /usr/local/src/slurm \
    && tar jxf slurm.tar.bz2 -C /usr/local/src/slurm --strip-components=1 \
    && rm slurm.tar.bz2 \
    && cd /usr/local/src/slurm \
    && ./configure --enable-debug --prefix=/usr --sysconfdir=/etc/slurm \
        --libdir=/usr/lib64 \
    && make install

# Required directories
RUN mkdir -p /var/run/munge \
    && chown -R munge:munge /var/run/munge \
    && chown -R munge:munge /var/log/munge \
    && chmod -R 770 /var/log/munge

# Allow jupyter user to launch munged
RUN usermod -G munge -a $NB_USER \
    && echo "$NB_USER    ALL=(munge) NOPASSWD: /usr/sbin/munged" > /etc/sudoers.d/munge \
    && chmod 0440 /etc/sudoers.d/munge \
    && chown root:root /etc/sudoers.d/munge

# Run container as
USER $NB_USER