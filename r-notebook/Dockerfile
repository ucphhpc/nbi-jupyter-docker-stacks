FROM nielsbohr/base-notebook:47be49899230
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60
ARG RSTUDIO_VERSION=1.1.453
ARG SHINY_VERSION=1.5.8.920

USER root

# Setup default timeout of installing packages
RUN echo "[global]" > /etc/pip.conf \
    && echo "timeout=$PACKAGE_TIMEOUT" >> /etc/pip.conf


# R-Studio install - with some extra fonts for LaTeX PDF generation
RUN apt-get update \
    && apt-get install -y fonts-dejavu lmodern cm-super unixodbc unixodbc-dev r-cran-rodbc \
    && wget https://download2.rstudio.org/rstudio-server-${RSTUDIO_VERSION}-amd64.deb -O /tmp/rstudio-server.deb \
    && wget https://download3.rstudio.org/ubuntu-14.04/x86_64/shiny-server-${SHINY_VERSION}-amd64.deb -O /tmp/shiny-server.deb \
    && apt-get install -y --no-install-recommends /tmp/rstudio-server.deb /tmp/shiny-server.deb \
    && rm /tmp/rstudio-server.deb /tmp/shiny-server.deb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV R_PATH=$CONDA_DIR/envs/r

WORKDIR /tmp

USER $NB_UID

RUN conda config --set remote_read_timeout_secs $PACKAGE_TIMEOUT

# Provide rstudio and shiny launcher icons
RUN pip install jupyter-rsession-proxy \
    && rm -fr /tmp/tmp* \
    && rm -fr /tmp/npm* \
    && rm -fr /tmp/v8* \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Create R environment
RUN conda create -n r \
    'gxx_linux-64' \
    'libgfortran' \
    'r-base=3.6.1' \
    'r-boot=1.3*' \
    'r-caret=6.0*' \
    'r-crayon=1.3*' \
    'r-devtools=2.0*' \
    'r-e1071=1.*' \
    'r-forecast=8.7*' \
    'r-hexbin=1.27*' \
    'r-htmltools=0.3*' \
    'r-htmlwidgets=1.3*' \
    'r-irkernel=1.0*' \
    'r-keras=2.2.*' \
    'r-leaps=3.*' \
    'r-nycflights13=1.0*' \
    'r-pheatmap=1.0*' \
    'r-plyr=1.8*' \
    'r-randomforest=4.6*' \
    'r-RColorBrewer=1.*' \
    'r-rcurl=1.95*' \
    'r-readr=1.3*' \
    'r-reshape2=1.4*' \
    'r-rjson=0.2*' \
    'r-rmarkdown=1.14*' \
    'r-rocr=1.*' \
    'r-rodbc=1.3*' \
    'r-rsqlite=2.1*' \
    'r-rtsne=0.*' \
    'r-shiny=1.3*' \
    'r-sparklyr=1.0*' \
    'r-tidyverse=1.2*' \
    'unixodbc=2.3.*' \
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

USER root

# Ensure that R can find it's required binaries
RUN echo "PATH=\"$R_PATH/bin:$PATH\"" >> /home/$NB_USER/.bashrc \
    && echo "PATH=\"/home/$NB_USER/.local/bin:$R_PATH/bin:$PATH\"" >> $R_PATH/lib/R/etc/Renviron \
    && rm -fr /usr/bin/python2 \
    && rm -fr /usr/bin/python2.7 \
    && rm -fr /usr/bin/python3.6m \
    && ln -s /usr/lib/rstudio-server/bin/rserver /usr/local/bin/rserver \
    && ln -s $R_PATH/bin/R /usr/local/bin/R

ENV LD_LIBRARY_PATH="/usr/lib"
WORKDIR /home/$NB_USER

# Ensure that container Runs as
USER $NB_UID
