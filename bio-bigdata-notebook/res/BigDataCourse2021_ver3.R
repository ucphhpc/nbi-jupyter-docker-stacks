## Installing CRAN packages
install.packages(c(
    "hexbin",
    "ggplot2",
    "pheatmap",
    "plyr",
    "FactoMineR",
    "factoextra",
    "dplyr",
    "tidyr",
    "magick",
    "magrittr",
    "gridExtra",
    "corpcor",
    "rmarkdown",
    "tinytex"
), repos='http://mirrors.dotsrc.org/cran/')
tinytex::install_tinytex()

# Installing packages from Bioconductor
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager", repos='http://mirrors.dotsrc.org/cran/')

library(BiocManager)

BiocManager::install("DESeq2", update = TRUE, ask = FALSE)
BiocManager::install("dada2", update = TRUE, ask = FALSE)
BiocManager::install("vsn", update = TRUE, ask = FALSE)
BiocManager::install("multtest", update = TRUE, ask = FALSE)
BiocManager::install("xcms", update = TRUE, ask = FALSE)
BiocManager::install("BiocParallel", update = TRUE, ask = FALSE)
BiocManager::install("CAMERA", update = TRUE, ask = FALSE)
BiocManager::install("pcaMethods",update = TRUE, ask = FALSE)
BiocManager::install("apeglm", update = TRUE, ask = FALSE)
BiocManager::install("xcms", update = TRUE, ask = FALSE)