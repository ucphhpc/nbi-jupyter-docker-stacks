FROM nielsbohr/base-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"

USER root

# R-Studio install
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    wget \
    #&& rstudio_version=$(wget --no-check-certificate -qO- https://s3.amazonaws.com/rstudio-server/current.ver) \
    && rstudio_version=1.1.463 \
    && wget https://download2.rstudio.org/rstudio-server-${rstudio_version}-amd64.deb -O /rstudio-server.deb \
    && apt-get install -y --no-install-recommends /rstudio-server.deb \
    && rm /rstudio-server.deb \
    && apt-get remove -y wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# R-studio env
ENV PATH="${PATH}:/usr/lib/rstudio-server/bin:/opt/conda/envs/r/bin"
ENV RSTUDIO_WHICH_R="/opt/conda/envs/r/bin/R"

USER $NB_UID

# R-Studio button
RUN git clone https://github.com/rasmunk/nbrsessionproxy.git /tmp/nbrsessionproxy \
    && pip install -e /tmp/nbrsessionproxy \
    && jupyter serverextension enable --py nbrsessionproxy \
    && jupyter labextension link /tmp/nbrsessionproxy/jupyterlab-rsessionproxy \
    && jupyter lab build

# Create R environment
RUN conda create -n r \
    && conda install -qy -n r \
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
    && conda clean -tipsy \
    && /opt/conda/envs/r/bin/R -e 'IRkernel::installspec()'

# Keras needs to find 'python' that has keras installed and not the system default
ENV PATH="/opt/conda/envs/python3/bin:${PATH}"
# RStudio dosen't work with the provided libssl.so.1.0.0, override the one
# provided by the system
RUN ln -s -f /usr/lib/x86_64-linux-gnu/libssl.so.1.0.0 /opt/conda/envs/r/lib/libssl.so.1.0.0

USER root

RUN fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Ensure that container Runs as
USER $NB_UID
