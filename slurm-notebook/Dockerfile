FROM nielsbohr/base-notebook:latest
MAINTAINER Rasmus Munk <rasmus.munk@nbi.ku.dk>

USER root

RUN groupadd -r slurm --gid=990 && useradd -r -g slurm --uid=990 slurm \
    && groupadd -r munge --gid=993 && useradd -r -g munge --uid=997 munge

# Dep
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    slurm-client \
    libslurm-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Required directories
RUN mkdir -p /var/run/munge \
    && chown munge:munge /var/run/munge

# TODO, run sudo -u munge munged on launch

# Run container as
USER $NB_USER