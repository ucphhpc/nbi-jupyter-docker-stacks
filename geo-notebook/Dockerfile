FROM nielsbohr/datascience-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"

USER root

# For GDAL
RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    proj-bin \
    g++ \
    software-properties-common \
    && add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable \
    && apt-get update \
    && apt-get install -yq --no-install-recommends \
    gdal-bin \
    libgdal-dev \
    && add-apt-repository --remove ppa:ubuntugis/ubuntugis-unstable \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER $NB_USER

RUN $PYTHON2_PATH/bin/pip install \
    Cartopy \
    geopandas \
    geoviews \
    iris \
    nco \
    GDAL==2.3.3 \
    && $PYTHON3_PATH/bin/pip install \
    Cartopy \
    geopandas \
    geoviews \
    gsw \
    nco \
    GDAL==2.3.3
