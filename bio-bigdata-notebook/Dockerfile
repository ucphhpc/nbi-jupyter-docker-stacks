FROM nielsbohr/r-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60

USER root

# Setup default timeout of installing packages
RUN echo "[global]" > /etc/pip.conf \
    && echo "timeout=$PACKAGE_TIMEOUT" >> /etc/pip.conf

# Install xcms
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    libnetcdf-dev \
    libc6-dev-i386 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# NOTE: install extras directly from github and CRAN as requested in erda ticket #18198
# IMPORTANT: R defaults to unpack with non-existant /bin/gtar so we overrride
ENV TAR="/bin/tar"

# install tmp r packages
COPY ./res /opt/res
RUN $R_PATH/bin/Rscript /opt/res/*.R

WORKDIR /home/$NB_USER

# Run container as
USER $NB_UID
