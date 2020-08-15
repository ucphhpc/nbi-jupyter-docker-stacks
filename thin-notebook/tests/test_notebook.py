from subprocess import Popen, PIPE, STDOUT


def test_notebook():
    p = Popen(["start-notebook.sh"], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    running = False
    for line in p.stdout:
        if "The Jupyter Notebook is running at" in str(line):
            running = True
            break

    assert running
