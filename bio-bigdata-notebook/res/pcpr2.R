install.packages(
    "devtools",
    repos=c("https://cloud.r-project.org", "https://mirrors.dotsrc.org/cran/")
)
library(devtools)

install_github(
    "JoeRothwell/pcpr2",
    force = TRUE,
    upgrade = "never"
)