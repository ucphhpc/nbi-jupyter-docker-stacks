FROM nielsbohr/r-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60

USER root

# Setup default timeout of installing packages
RUN echo "[global]" > /etc/pip.conf \
    && echo "timeout=$PACKAGE_TIMEOUT" >> /etc/pip.conf

# R-studio envs provided by r-notebook
# BioBase dependency
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gfortran \
    libxml2-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp

USER $NB_UID

RUN conda config --set remote_read_timeout_secs $PACKAGE_TIMEOUT

# Standard CRAN packages, etc.
RUN conda install -qy -n r \
    'r-FactoMineR' \
    'r-factoextra' \
    'r-fastICA' \
    'r-ggplot2' \
    'r-gridExtra' \
    'r-vegan' \
    'r-alluvial' \
    'r-ade4' \
    'r-lsmeans' \
    'r-eulerr' \
    'r-tibble' \
    'r-readxl' \
    'r-plyr' \
    'r-dplyr' \
    'r-reshape2' \
    'r-stringr' \
    'r-pscl' \
    'r-statmod' \
    'r-picante' \
    'r-nlme' \
    'r-lme4' \
    'r-cowplot' \
    'r-doParallel' \
    'r-doSNOW' \
    'r-pROC' \
    'r-ape' \
    'r-minpack.lm' \
    && conda clean --all -f -y \
    && /opt/conda/envs/r/bin/R -e 'IRkernel::installspec()' \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# NOTE: install BioConductor packages requested e.g. in erda ticket #18198
## BioConductor packages, etc.
RUN conda install -qy -c bioconda -n r \
    'r-phytools' \
    'bioconductor-deseq2' \
    'bioconductor-biobase' \
    'bioconductor-tximport' \
    'bioconductor-sva' \
    'bioconductor-preprocesscore' \
    'bioconductor-edaseq' \
    'bioconductor-msa' \
    'bioconductor-phyloseq' \
    'bioconductor-dada2' \
    'bioconductor-edgeR' \
    'bioconductor-metagenomeSeq' \
    'bioconductor-limma' \
    'bioconductor-Biostrings' \
    'bioconductor-biocinstaller' \
    'cutadapt' \
    'mafft' \
    'fasttree' \
    && conda clean --all -f -y \
    && /opt/conda/envs/r/bin/R -e 'IRkernel::installspec()' \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

ENV PATH="/home/$NB_USER/.local/bin:$R_PATH/bin:$PATH"

# NOTE: install extras directly from github and CRAN as requested in erda ticket #18198
# IMPORTANT: R defaults to unpack with non-existant /bin/gtar so we overrride
ENV TAR="/bin/tar"
RUN /opt/conda/envs/r/bin/Rscript -e 'library(devtools); options(unzip = "internal"); devtools::install_github("Russel88/DAtest@v2.7.13", force = TRUE); install_github("DanielSprockett/reltools", force = TRUE); install.packages("ips", repos="http://mirrors.dotsrc.org/cran/")'

WORKDIR /home/$NB_USER

# Run container as
USER $NB_UID
