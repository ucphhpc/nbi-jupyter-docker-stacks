import os
import subprocess
import tempfile
import nbformat

cur_path = os.path.abspath(".")
notebooks_path = os.path.join(cur_path, "notebooks")
python_notebooks_path = os.path.join(notebooks_path, "python")
r_notebooks_path = os.path.join(notebooks_path, "r")


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


def test_python_notebooks():
    for f_notebook in os.listdir(python_notebooks_path):
        _, errors = _notebook_run(
            os.path.join(python_notebooks_path, f_notebook), kernel="python"
        )
        assert errors == []


def test_r_notebooks():
    for f_notebook in os.listdir(r_notebooks_path):
        _, errors = _notebook_run(
            os.path.join(r_notebooks_path, f_notebook), kernel="ir"
        )
        assert errors == []
