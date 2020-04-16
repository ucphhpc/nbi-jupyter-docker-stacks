## CRAN packages.

# Provided by #21911: Update Bio Notebook on ERDA jupyter

install.packages(c(
    "devtools",
    "ggplot2",
    "phytools",
    "gridExtra",
    "vegan",
    "alluvial",
    "ade4",
    "lsmeans",
    "eulerr",
    "tibble",
    "readxl",
    "RColorBrewer",
    "plyr",
    "dplyr",
    "reshape2",
    "stringr",
    "pscl",
    "statmod",
    "picante",
    "nlme",
    "lme4",
    "cowplot",
    "doParallel",
    "doSNOW",
    "pROC",
    "ape",
    "minpack.lm",
    "ips",
    "BiocManager"
), repos='http://mirrors.dotsrc.org/cran/')

## BioConductor packages.
BiocManager::install(c(
    "msa",
    "phyloseq",
    "dada2",
    "edgeR",
    "metagenomeSeq",
    "limma",
    "Biostrings"
), update = FALSE)

library(devtools);
options(unzip = "internal");
## GitHub packages.
devtools::install_github("Russel88/DAtest", force = TRUE, upgrade = "never")
devtools::install_github("Russel88/MicEco", force = TRUE, upgrade = "never")
devtools::install_github("Russel88/COEF", force = TRUE, upgrade = "never")
install_github("DanielSprockett/reltools", force = TRUE);

pkgs <- list(
    "ggplot2",
    "phytools",
    "gridExtra",
    "vegan",
    "alluvial",
    "ade4",
    "lsmeans",
    "eulerr",
    "tibble",
    "readxl",
    "RColorBrewer",
    "plyr",
    "dplyr",
    "reshape2",
    "stringr",
    "pscl",
    "statmod",
    "picante",
    "nlme",
    "lme4",
    "cowplot",
    "doParallel",
    "doSNOW",
    "pROC",
    "ape",
    "minpack.lm",
    "msa",
    "phyloseq",
    "dada2",
    "edgeR",
    "metagenomeSeq",
    "limma",
    "Biostrings",
    "DAtest",
    "MicEco",
    "COEF",
    "ips")

for(i in pkgs){
    requireNamespace(i)
}

