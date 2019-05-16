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
    && conda clean -tipsy \
    && fix-permissions $CONDA_DIR \
    && /opt/conda/envs/r/bin/R -e 'IRkernel::installspec()'

# NOTE: install extras directly from github and CRAN as requested in erda ticket #18198
# IMPORTANT: R defaults to unpack with non-existant /bin/gtar so we overrride
ENV TAR="/bin/tar"
RUN /opt/conda/envs/r/bin/Rscript -e 'library(devtools); options(unzip = "internal"); devtools::install_github("Russel88/DAtest", force = TRUE); install_github("DanielSprockett/reltools", force = TRUE); install.packages("ips", repos="http://mirrors.dotsrc.org/cran/")'

# Run container as
USER $NB_USER
