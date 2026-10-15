## CRAN packages.
# Install the packages that are not available on conda
install.packages(c(
    "fasttree",
    "ips",
    "multicomp"
), repos=c("https://cloud.r-project.org", "https://mirrors.dotsrc.org/cran/"))

options(unzip = "internal");
## GitHub packages.
remotes::install_github("Russel88/DAtest", force = TRUE, upgrade = "never")
remotes::install_github("Russel88/MicEco", force = TRUE, upgrade = "never")
remotes::install_github("Russel88/COEF", force = TRUE, upgrade = "never")
remotes::install_github("DanielSprockett/reltools", force = TRUE);
