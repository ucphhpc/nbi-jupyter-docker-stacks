from notebooks import *

NOTEBOOKS_ARCHITECTURE = {
    BASE_NOTEBOOK_LATEST: {
        "parent": None
    },
    PYTHON_NOTEBOOK_LATEST: {
        "parent": BASE_NOTEBOOK_LATEST,
    },
    R_NOTEBOOK_LATEST: {
        "parent": PYTHON_NOTEBOOK_LATEST
    },
    SLURM_NOTEBOOK_LATEST: {
        "parent": PYTHON_NOTEBOOK_LATEST
    },
    SLURM_NOTEBOOK_20_02_07: {
        "parent": PYTHON_NOTEBOOK_LATEST
    },
    SLURM_NOTEBOOK_21_08_0: {
        "parent": PYTHON_NOTEBOOK_LATEST
    },
    PYTHON_CUDA_NOTEBOOK_LATEST: {
        "parent": PYTHON_NOTEBOOK_LATEST
    },
    GPU_NOTEBOOK_LATEST: {
        "parent": PYTHON_CUDA_NOTEBOOK_LATEST
    },
    DGX1_NOTEBOOK_LATEST: {
        "parent": GPU_NOTEBOOK_LATEST
    },
    DATASCIENCE_NOTEBOOK_LATEST: {
        "parent": PYTHON_NOTEBOOK_LATEST
    },
    CHEMISTRY_NOTEBOOK_LATEST: {
        "parent": BASE_NOTEBOOK_LATEST
    },
    FENICS_NOTEBOOK_LATEST: {
        "parent": PYTHON_NOTEBOOK_LATEST
    },
    QSHARP_NOTEBOOK_LATEST: {
        "parent": PYTHON_NOTEBOOK_LATEST
    },
    STATISTICS_NOTEBOOK_LATEST: {
        "parent": PYTHON_NOTEBOOK_LATEST
    },
    TOMOGRAPHY_NOTEBOOK_LATEST: {
        "parent": PYTHON_NOTEBOOK_LATEST
    },
    HPC_NOTEBOOK_LATEST: {
        "parent": SLURM_NOTEBOOK_LATEST
    },
    HPC_NOTEBOOK_20_02_07: {
        "parent": SLURM_NOTEBOOK_20_02_07
    },
    HPC_NOTEBOOK_21_08_0: {
        "parent": SLURM_NOTEBOOK_21_08_0
    },
    HPC_OCEAN_NOTEBOOK_LATEST: {
        "parent": SLURM_NOTEBOOK
    },
    HPC_OCEAN_NOTEBOOK_20_02_07: {
        "parent": SLURM_NOTEBOOK_20_02_07
    },
    HPC_OCEAN_NOTEBOOK_21_08_0: {
        "parent": SLURM_NOTEBOOK_21_08_0
    },
    OCEAN_NOTEBOOK_LATEST: {
        "parent": DATASCIENCE_NOTEBOOK_LATEST
    },
    GEO_NOTEBOOK_LATEST: {
        "parent": PYTHON_NOTEBOOK_LATEST
    },
    BIO_NOTEBOOK_LATEST: {
        "parent": R_NOTEBOOK_LATEST
    },
    BIO_BIGDATA_NOTEBOOK_LATEST: {
        "parent": R_NOTEBOOK_LATEST
    },
    BIO_BSA_NOTEBOOK: {
        "parent": R_NOTEBOOK_LATEST
    },
    SME_NOTEBOOK_LATEST: {
        "parent": BASE_NOTEBOOK_LATEST
    },
    JWST_NOTEBOOK_LATEST: {
        "parent": PYTHON_NOTEBOOK_LATEST
    }
}