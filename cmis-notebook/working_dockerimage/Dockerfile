FROM continuumio/miniconda3

RUN conda init bash
RUN conda create -n py39 python=3.9 conda-forge::meshplot conda-forge::wildmeshing matplotlib scipy numpy conda-forge::igl pip ipympl jupyter


RUN echo "source activate py39" > ~/.bashrc
ENV PATH /opt/conda/envs/env/bin:$PATH
RUN mkdir -p /opt/notebooks

CMD ["bash", "-c", "/opt/conda/envs/py39/bin/jupyter lab \
    --notebook-dir=/opt/notebooks --ip='*' --port=8888 \
    --no-browser --allow-root"]
