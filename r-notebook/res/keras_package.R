
# CRAN packages
install.packages("keras3", repos="https://mirrors.dotsrc.org/cran/")
library(keras3)

# install_keras uses reticulate to discover the Python environment
# Therefore python_version can also be an absolute path to a python binary
# https://github.com/rstudio/reticulate/blob/56ea74e810f3b2fca3b67a973414624933e09a37/R/virtualenv.R#L503
install_keras(
    python_version = Sys.getenv("RETICULATE_PYTHON"),
    backend=c("tensorflow", "jax"),
    restart_session=FALSE
)
