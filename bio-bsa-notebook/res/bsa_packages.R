# Installing packages from Bioconductor
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager", repos='http://mirrors.dotsrc.org/cran/')

library(BiocManager)

BiocManager::install("bwa", update = TRUE, ask = FALSE)
BiocManager::install("emboss", update = TRUE, ask = FALSE)
BiocManager::install("blast", update = TRUE, ask = FALSE)
BiocManager::install("clustalw", update = TRUE, ask = FALSE)
BiocManager::install("fastqc", update = TRUE, ask = FALSE)
BiocManager::install("hmmer", update = TRUE, ask = FALSE)
BiocManager::install("mem", update = TRUE, ask = FALSE)