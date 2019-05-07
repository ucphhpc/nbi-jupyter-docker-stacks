import os
import subprocess
import tempfile
import nbformat

cur_path = os.path.abspath(".")
notebooks_path = os.path.join(cur_path, 'notebooks')
kernels = ['python2', 'python3']


def _notebook_run(path, kernel='python3'):
    """Execute a notebook via nbconvert and collect output.
       :returns (parsed nb object, execution errors)
    """
    dirname, __ = os.path.split(path)
    os.chdir(dirname)
    with tempfile.NamedTemporaryFile(suffix=".ipynb") as fout:
        args = ["jupyter", "nbconvert", "--to", "notebook", "--execute",
                "--ExecutePreprocessor.timeout=300",
                "--ExecutePreprocessor.kernel_name=" + kernel,
                "--output", fout.name, path]
        subprocess.check_call(args)

        fout.seek(0)
        nb = nbformat.read(fout, nbformat.current_nbformat)

    errors = [output for cell in nb.cells if "outputs" in cell
              for output in cell["outputs"]
              if output.output_type == "error"]

    return nb, errors


# List of notebooks which require CUDA and thus special handling
cuda_notebooks = ['tensorflow.ipynb',
                  'keras.ipynb',
                  'keras-contrib.ipynb']


def test_notebooks():
    for f_notebook in os.listdir(notebooks_path):
        # skip special notebooks
        if f_notebook in cuda_notebooks:
            continue
        for kernel in kernels:
            _, errors = _notebook_run(os.path.join(notebooks_path,
                                                   f_notebook), kernel=kernel)
            assert errors == []


def test_cuda_notebooks():
    """Requires that cuda is available, if not don't run"""
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
        """Requires that cuda is available, if not don't run"""
        notebooks_paths = [os.path.join(notebooks_path, i)
                           for i in cuda_notebooks]
        for notebook_path in notebooks_paths:
            for kernel in kernels:
                _, errors = _notebook_run(notebook_path, kernel)
                assert errors == []
