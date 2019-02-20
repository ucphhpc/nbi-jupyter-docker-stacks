FROM nielsbohr/datascience-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"

USER root

# For opencv2 and basemap geos
RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    proj-bin \
    libgdal-dev \
    build-essential \
    g++ \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER $NB_USER

RUN $PYTHON2_PATH/bin/pip install \
    Cartopy \
    geopandas \
    geoviews \
    iris \
    nco \
    && $PYTHON3_PATH/bin/pip install \
    Cartopy \
    geopandas \
    geoviews \
    gsw \
    nco

RUN $PYTHON2_PATH/bin/pip install \
    GDAL==2.3.2 \
    && $PYTHON3_PATH/bin/pip install \
    GDAL==2.3.2
