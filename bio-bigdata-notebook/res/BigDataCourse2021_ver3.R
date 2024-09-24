## Installing CRAN packages
install.packages(c(
    "circlize",
    "hexbin",
    "ggplot2",
    "pheatmap",
    "plyr",
    "plotly",
    "FactoMineR",
    "Factoshiny",
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
tinytex::install_tinytex(force=TRUE)

# Installing packages from Bioconductor
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager", repos='http://mirrors.dotsrc.org/cran/')

library(BiocManager)
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

library(devtools)
devtools::install_github("JoeRothwell/pcpr2", force = TRUE, upgrade = "never")