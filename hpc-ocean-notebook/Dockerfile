FROM nielsbohr/slurm-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    libnetcdf-dev \
    libnetcdff-dev \
    libnetcdff-doc \
    libnetcdf-dev \
    libhdf5-dev \
    && apt-get clean \
    && rm -fr /var/lib/apt/lists/*

WORKDIR /tmp 

USER $NB_UID

COPY requirements.txt /tmp/
RUN conda run -n python3 pip install -r requirements.txt \
    && conda clean -y --all \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

WORKDIR /home/$NB_USER
# As an exception, run as root,
# Remember to use supervisord start-notebook.sh to
# de-escalate privileges to $NB_UID:$NB_GID
USER root
