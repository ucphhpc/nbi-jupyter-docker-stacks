import os
import subprocess
import tempfile
import nbformat

cur_path = os.path.abspath(".")
notebooks_path = os.path.join(cur_path, "notebooks")
gpu_notebooks_path = os.path.join(cur_path, "gpu_notebooks")
kernels = ["python3"]


def _notebook_run(path, kernel="python3", timeout=60):
    """Execute a notebook via nbconvert and collect output.
    :returns (parsed nb object, execution errors)
    """
    dirname, __ = os.path.split(path)
    os.chdir(dirname)
    with tempfile.NamedTemporaryFile(suffix=".ipynb") as fout:
        args = [
            "jupyter",
            "nbconvert",
            "--to",
            "notebook",
            "--execute",
            "--ExecutePreprocessor.timeout={}".format(timeout),
            "--ExecutePreprocessor.kernel_name={}".format(kernel),
            "--output",
            fout.name,
            path,
        ]
        subprocess.check_call(args)

        fout.seek(0)
        nb = nbformat.read(fout, nbformat.current_nbformat)

    errors = [
        output
        for cell in nb.cells
        if "outputs" in cell
        for output in cell["outputs"]
        if output.output_type == "error"
    ]

    return nb, errors


def test_cpu_notebooks():
    for f_notebook in os.listdir(notebooks_path):
        for kernel in kernels:
            _, errors = _notebook_run(
                os.path.join(notebooks_path, f_notebook), kernel=kernel, timeout=360
            )
            assert errors == []


def test_gpu_notebooks():
    """Requires that gpu is available, if not don't run"""
    try:
        import tensorflow as tf
    except ImportError as err:
        print("Failed to import tensorflow: ", err)
        return 0
    avail = tf.test.is_gpu_available()

    if not avail:
        print("No gpus were available, skipped test")
        return 0

    if avail:
        """Requires that gpu is available, if not don't run"""
        for notebook_path in gpu_notebooks_path:
            for kernel in kernels:
                _, errors = _notebook_run(os.path.join(gpu_notebooks_path, notebook_path), kernel, timeout=360)
                assert errors == []
