
## CRAN packages.
# Provided by #34549
install.packages(
    "devtools",
    repos=c("https://cloud.r-project.org", "https://mirrors.dotsrc.org/cran/")
)
library(devtools)

install_github("DoseResponse/drcData", dependencies=TRUE, force=TRUE)
install_github("DoseResponse/drc", dependencies=TRUE, force=TRUE)
install_github("DoseResponse/bmd", dependencies=TRUE, force=TRUE)
