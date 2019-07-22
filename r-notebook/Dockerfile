FROM nielsbohr/base-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60
ARG RSTUDIO_VERSION=1.1.463

USER root

# Setup default timeout of installing packages
RUN echo "[global]" > /etc/pip.conf \
    && echo "timeout=$PACKAGE_TIMEOUT" >> /etc/pip.conf

# R-Studio install
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    wget \
    && wget https://download2.rstudio.org/rstudio-server-${RSTUDIO_VERSION}-amd64.deb -O /rstudio-server.deb \
    && apt-get install -y --no-install-recommends /rstudio-server.deb \
    && rm /rstudio-server.deb \
    && apt-get remove -y wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV R_PATH=$CONDA_DIR/envs/r

WORKDIR /tmp

USER $NB_UID

RUN conda config --set remote_read_timeout_secs $PACKAGE_TIMEOUT

# R-Studio button
RUN git clone https://github.com/rasmunk/nbrsessionproxy.git /opt/nbrsessionproxy \
    && pip install -e /opt/nbrsessionproxy \
    && jupyter serverextension enable --py nbrsessionproxy \
    && jupyter labextension link /opt/nbrsessionproxy/jupyterlab-rsessionproxy \
    && jupyter lab build \
    && rm -fr /tmp/tmp* \
    && rm -fr /tmp/npm* \
    && rm -fr /tmp/v8* \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Create R environment
RUN conda create -n r \
    'r-base=3.5.1' \
    'r-irkernel=1.0*' \
    'r-plyr=1.8*' \
    'r-devtools=2.0*' \
    'r-tidyverse=1.2*' \
    'r-shiny=1.3*' \
    'r-rmarkdown=1.13*' \
    'r-forecast=8.7*' \
    'r-rsqlite=2.1*' \
    'r-reshape2=1.4*' \
    'r-nycflights13=1.0*' \
    'r-caret=6.0*' \
    'r-rcurl=1.95*' \
    'r-crayon=1.3*' \
    'r-randomforest=4.6*' \
    'r-htmltools=0.3*' \
    'r-sparklyr=1.0*' \
    'r-htmlwidgets=1.3*' \
    'r-hexbin=1.27*' \
    'r-keras=2.2*' \
    'r-e1071=1.7*' \
    'r-rocr=1.0*' \
    'r-RColorBrewer' \
    'r-pheatmap' \
    'r-readr' \
    'r-rjson' \
    && conda clean --all -f -y \
    && $R_PATH/bin/R -e 'IRkernel::installspec()' \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

RUN jupyter kernelspec uninstall -f python3 \
    && rm -fr $CONDA_DIR/lib/python3.7/site-packages/ipykernel

RUN conda install -n r \
    ipykernel \
    tensorflow \
    && $R_PATH/bin/python -m ipykernel install --user \
    && conda clean --all -f -y \
    && rm -fr /tmp/tmp* \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Setup user env path links
RUN mkdir -p /home/$NB_USER/.local/bin \
    && ln -s $R_PATH/bin/R /home/$NB_USER/.local/bin/R \
    && ln -s $R_PATH/bin/python /home/$NB_USER/.local/bin/python \
    && ln -s $R_PATH/bin/python3 /home/$NB_USER/.local/bin/python3 \
    && ln -s $R_PATH/bin/python3.7 /home/$NB_USER/.local/bin/python3.7 \
    && ln -s $R_PATH/bin/python3.7-config /home/$NB_USER/.local/bin/python3.7-config \
    && ln -s $R_PATH/bin/python3.7m /home/$NB_USER/.local/bin/python3.7m \
    && ln -s $R_PATH/bin/python3.7m-config /home/$NB_USER/.local/bin/python3.7m-config \
    && ln -s $R_PATH/bin/python3-config /home/$NB_USER/.local/bin/python3-config \
    && ln -s $R_PATH/bin/pip /home/$NB_USER/.local/bin/pip

# RStudio dosen't work with the provided libssl.so.1.0.0, override the one
# provided by the system
RUN ln -s -f /usr/lib/x86_64-linux-gnu/libssl.so.1.0.0 /opt/conda/envs/r/lib/libssl.so.1.0.0

USER root

# Ensure that RStudio can find it's required binaries
RUN echo "PATH=\"/home/$NB_USER/.local/bin:$PATH\"" >> /home/$NB_USER/.bashrc \
    && rm -fr /usr/bin/python2 \
    && rm -fr /usr/bin/python2.7 \
    && rm -fr /usr/bin/python3.6m \
    && ln -s /usr/lib/rstudio-server/bin/rserver /usr/local/bin/rserver \
    && ln -s $R_PATH/bin/R /usr/local/bin/R

WORKDIR /home/$NB_USER

# Ensure that container Runs as
USER $NB_UID
