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
), repos='http://mirrors.dotsrc.org/cran/')
tinytex::install_tinytex(force=TRUE)

# Installing packages from Bioconductor
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager", repos='http://mirrors.dotsrc.org/cran/')

library(BiocManager)
BiocManager::install("tximport", update = TRUE, ask = FALSE, force = TRUE)
BiocManager::install("sva", update = TRUE, ask = FALSE, force = TRUE)
BiocManager::install("preprocesscore", update = TRUE, ask = FALSE, force = TRUE)
BiocManager::install("edaseq", update = TRUE, ask = FALSE, force = TRUE)
BiocManager::install("msa", update = TRUE, ask = FALSE, force = TRUE)
BiocManager::install("phyloseq", update = TRUE, ask = FALSE, force = TRUE)
BiocManager::install("edgeR", update = TRUE, ask = FALSE, force = TRUE)
BiocManager::install("metagenomeSeq", update = TRUE, ask = FALSE, force = TRUE)
BiocManager::install("limma", update = TRUE, ask = FALSE, force = TRUE)
BiocManager::install("Biostrings", update = TRUE, ask = FALSE, force = TRUE)
BiocManager::install("biocinstaller", update = TRUE, ask = FALSE, force = TRUE)
BiocManager::install("DESeq2", update = TRUE, ask = FALSE, force = TRUE)
BiocManager::install("dada2", update = TRUE, ask = FALSE, force = TRUE)
BiocManager::install("vsn", update = TRUE, ask = FALSE, force = TRUE)
BiocManager::install("multtest", update = TRUE, ask = FALSE, force = TRUE)
BiocManager::install("xcms", update = TRUE, ask = FALSE, force = TRUE)
BiocManager::install("BiocParallel", update = TRUE, ask = FALSE, force = TRUE)
BiocManager::install("CAMERA", update = TRUE, ask = FALSE, force = TRUE)
BiocManager::install("pcaMethods",update = TRUE, ask = FALSE, force = TRUE)
BiocManager::install("apeglm", update = TRUE, ask = FALSE, force = TRUE)
# Added additional packages based on requests made in ticket #31641
BiocManager::install("GWENA", update = TRUE, ask = FALSE, force = TRUE)
