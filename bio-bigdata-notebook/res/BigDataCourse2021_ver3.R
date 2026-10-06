## Installing CRAN packages
install.packages(c(
    "circlize",
    "hexbin",
    "ggplot2",
    "pheatmap",
    "plyr",
    "plotly",
    "phytools",
    "fasttree",
    "FactoMineR",
    "Factoshiny",
    "factoextra",
    "dplyr",
    "tidyr",
    "mafft",
    "magick",
    "magrittr",
    "gridExtra",
    "corpcor",
    "rmarkdown",
    "tinytex"
), repos=c("https://cloud.r-project.org", "https://mirrors.dotsrc.org/cran/"))
tinytex::install_tinytex(force=TRUE)

# Installing packages from Bioconductor
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager", repos=c("https://cloud.r-project.org", "https://mirrors.dotsrc.org/cran/"))

library(BiocManager)
BiocManager::install(version = "3.20")
BiocManager::install(c(
    "tximport",
    "sva",
    "preprocesscore",
    "edaseq",
    "msa",
    "phyloseq",
    "edgeR",
    "metagenomeSeq",
    "limma",
    "Biostrings",
    "biocinstaller",
    "DESeq2",
    "dada2",
    "vsn",
    "multtest",
    "xcms",
    "BiocParallel",
    "CAMERA",
    "pcaMethods",
    "apeglm",
# Added additional packages based on requests made in ticket #31641
    "GWENA"
), update=TRUE, ask = FALSE, force = TRUE)

