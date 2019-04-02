FROM nielsbohr/r-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"

USER root

# R-studio env
ENV PATH="${PATH}:/usr/lib/rstudio-server/bin:/opt/conda/envs/r/bin"
ENV RSTUDIO_WHICH_R="/opt/conda/envs/r/bin/R"

USER root

# BioBase dependency
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    gfortran \
    libxml2-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER $NB_USER

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
    && conda clean -tipsy \
    && fix-permissions $CONDA_DIR \
    && /opt/conda/envs/r/bin/R -e 'IRkernel::installspec()'

## BioConductor packages, etc.
RUN conda install -qy -c bioconda -n r \
    'r-phytools' \
    'bioconductor-msa' \
    'bioconductor-phyloseq' \
    'bioconductor-dada2' \
    'bioconductor-edgeR' \
    'bioconductor-metagenomeSeq' \
    'bioconductor-limma' \
    'bioconductor-Biostrings' \
    && conda clean -tipsy \
    && fix-permissions $CONDA_DIR \
    && /opt/conda/envs/r/bin/R -e 'IRkernel::installspec()'

# TODO: install these two from github, too, as requested?
#       devtools::install_github("Russel88/DAtest", force = TRUE)
#       devtools::install_github("DanielSprockett/reltools", force = TRUE)

# bioLite and Biobase is from BioInfo, should be removed from image
RUN /opt/conda/envs/r/bin/R -e 'source("https://bioconductor.org/biocLite.R") ; \
biocLite(c("DESeq2","Biobase","tximport","sva","preprocessCore")) ; \
biocLite("EDASeq")'


# Run container as
USER $NB_USER
