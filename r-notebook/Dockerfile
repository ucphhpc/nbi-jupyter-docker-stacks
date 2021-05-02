FROM nielsbohr/python-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60
ARG RSTUDIO_VERSION=1.1.463
ARG SHINY_VERSION=1.5.8.922

USER root

# Setup default timeout of installing packages
RUN echo "[global]" > /etc/pip.conf \
    && echo "timeout=$PACKAGE_TIMEOUT" >> /etc/pip.conf

# R-Studio install - with some extra fonts for LaTeX PDF generation
# R-Studio also requires libssl1.0.{0,1} before it can be installed
# While Ubuntu 20.04 only provides > libssl1.1
RUN apt-get update \
    && apt-get install -y fonts-dejavu lmodern cm-super unixodbc unixodbc-dev \
    && wget http://security.ubuntu.com/ubuntu/pool/main/o/openssl1.0/libssl1.0.0_1.0.2n-1ubuntu5.6_amd64.deb \
    && dpkg -i libssl1.0.0_1.0.2n-1ubuntu5.6_amd64.deb \
    && rm -fr libssl1.0.0_1.0.2n-1ubuntu5.6_amd64.deb \
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
RUN jupyterlab_pip3 install jupyter-rsession-proxy \
    && rm -fr /tmp/tmp* \
    && rm -fr /tmp/npm* \
    && rm -fr /tmp/v8* \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Create R environment
RUN conda create -n r \
    'gxx_linux-64' \
    'libgfortran' \
    'r-base=4.0.3' \
    'r-boot=1.3*' \
    'r-caret=6.0*' \
    'r-crayon=1.4*' \
    'r-devtools=2.3*' \
    'r-e1071=1.*' \
    'r-forecast=8.14*' \
    'r-hexbin=1.28*' \
    'r-htmltools=0.5*' \
    'r-htmlwidgets=1.5*' \
    'r-irkernel=1.1*' \
    'r-keras=2.4.*' \
    'r-leaps=3.*' \
    'r-nycflights13=1.0*' \
    'r-pheatmap=1.0*' \
    'r-plyr=1.8*' \
    'r-randomforest=4.6*' \
    'r-RColorBrewer=1.*' \
    'r-rcurl=1.*' \
    'r-readr=1.4*' \
    'r-reshape2=1.4*' \
    'r-rjson=0.2*' \
    'r-rmarkdown=2.*' \
    'r-rocr=1.*' \
    'r-rodbc=1.3*' \
    'r-rsqlite=2.2*' \
    'r-rtsne=0.*' \
    'r-shiny=1.6*' \
    'r-sparklyr=1.6*' \
    'r-tidyverse=1.3*' \
    'r-v8=3.4.*' \
    'unixodbc=2.3.*' \
    && conda clean --all -f -y \
    && $R_PATH/bin/R -e 'IRkernel::installspec()' \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

RUN conda install -n r \
    python=3.7 \
    ipykernel \
    && $R_PATH/bin/python -m ipykernel install --user \
    && conda clean --all -f -y \
    && rm -fr /tmp/tmp* \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# install tmp r packages
COPY ./res /opt/res
RUN conda run -n r Rscript /opt/res/keras_package.R

USER root

# Ensure that R can find it's required binaries
RUN echo "PATH=\"$R_PATH/bin:$PATH\"" >> /home/$NB_USER/.bashrc \
    && echo "PATH=\"/home/$NB_USER/.local/bin:$R_PATH/bin:$PATH\"" >> $R_PATH/lib/R/etc/Renviron \
    && ln -s /usr/lib/rstudio-server/bin/rserver /usr/local/bin/rserver \
    && ln -s $R_PATH/bin/R /usr/local/bin/R
RUN python3 /usr/local/bin/update_kernel_spec.py ir --env-kwargs PATH=$R_PATH/bin:$PATH

WORKDIR /home/$NB_USER

# Ensure that container Runs as
USER $NB_UID
