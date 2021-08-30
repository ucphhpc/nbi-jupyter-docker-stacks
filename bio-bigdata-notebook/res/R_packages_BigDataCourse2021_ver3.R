## Installing CRAN packages
install.packages("tidyverse", dependencies = TRUE)
install.packages("hexbin", dependencies = TRUE)
install.packages("ggplot2", dependencies = TRUE)
install.packages("pheatmap", dependencies = TRUE)
install.packages("plyr", dependencies = TRUE)
install.packages("FactoMineR", dependencies = TRUE)
install.packages("factoextra", dependencies = TRUE)
install.packages("dplyr", dependencies = TRUE)
install.packages("tidyr", dependencies = TRUE)
install.packages("magick", dependencies = TRUE)
install.packages("magrittr", dependencies = TRUE)
install.packages("gridExtra", dependencies = TRUE)
install.packages("corpcor", dependencies = TRUE)
install.packages("rmarkdown", dependencies = TRUE)
install.packages("tinytex")
tinytex::install_tinytex()  # install TinyTeX

## Installing packages from Bioconductor
if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager")
library(BiocManager)

BiocManager::install("DESeq2", update = TRUE, ask = FALSE)
BiocManager::install("dada2", update = TRUE, ask = FALSE)
BiocManager::install("vsn", update = TRUE, ask = FALSE)
BiocManager::install("multtest", update = TRUE, ask = FALSE)
BiocManager::install("xcms", update = TRUE, ask = FALSE)
BiocManager::install("BiocParallel", update = TRUE, ask = FALSE)
BiocManager::install("CAMERA", update = TRUE, ask = FALSE)
BiocManager::install("pcaMethods",update = TRUE, ask = FALSE)


