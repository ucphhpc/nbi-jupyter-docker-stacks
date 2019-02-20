FROM nielsbohr/python-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"

USER root

# For opencv2 and basemap geos
RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER $NB_USER

ENV LD_LIBRARY_PATH=/opt/conda/lib

RUN conda install --name python3 -c conda-forge fenics==2018.1.0