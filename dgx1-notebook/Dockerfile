FROM nvidia/cuda:9.0-cudnn7-runtime
MAINTAINER Rasmus Munk <rasmus.munk@nbi.ku.dk>

USER root

# Taken from https://github.com/jupyter/docker-stacks/blob/master/base-notebook/Dockerfile
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get -yq dist-upgrade \
 	&& apt-get install -yq --no-install-recommends \
    wget \
    bzip2 \
    ca-certificates \
    sudo \
    locales \
    fonts-liberation \
    vim \
    nano \
    htop \
    screen \
    tmux \
    git \
    && apt-get clean \
 	&& rm -rf /var/lib/apt/lists/*

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

# Configure environment
ENV CONDA_DIR=/opt/conda \
    SHELL=/bin/bash \
    NB_USER=jovyan \
    NB_UID=1000 \
    NB_GID=100 \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8
ENV PATH=$CONDA_DIR/bin:$PATH \
    HOME=/home/$NB_USER

ADD fix-permissions /usr/local/bin/fix-permissions
# Create jovyan user with UID=1000 and in the 'users' group
# and make sure these dirs are writable by the `users` group.
RUN groupadd wheel -g 11 && \
    echo "auth required pam_wheel.so use_uid" >> /etc/pam.d/su && \
    useradd -m -s /bin/bash -N -u $NB_UID $NB_USER && \
    mkdir -p $CONDA_DIR && \
    chown $NB_USER:$NB_GID $CONDA_DIR && \
    chmod g+w /etc/passwd && \
    fix-permissions $HOME && \
    fix-permissions $CONDA_DIR

USER $NB_UID

# Setup work directory for backward-compatibility
RUN mkdir /home/$NB_USER/work && \
    fix-permissions /home/$NB_USER

# Install conda as jovyan and check the md5 sum provided on the download site
ENV MINICONDA_VERSION 4.5.4
RUN cd /tmp && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh && \
    echo "a946ea1d0c4a642ddf0c3a26a18bb16d *Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh" | md5sum -c - && \
    /bin/bash Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh -f -b -p $CONDA_DIR && \
    rm Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh && \
    $CONDA_DIR/bin/conda config --system --prepend channels conda-forge && \
    $CONDA_DIR/bin/conda config --system --set auto_update_conda false && \
    $CONDA_DIR/bin/conda config --system --set show_channel_urls true && \
    $CONDA_DIR/bin/conda install --quiet --yes conda="${MINICONDA_VERSION%.*}.*" && \
    $CONDA_DIR/bin/conda update --all --quiet --yes && \
    conda clean -tipsy && \
    rm -rf /home/$NB_USER/.cache/yarn && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

# Install Tini
RUN conda install --quiet --yes 'tini=0.18.0' && \
    conda list tini | grep tini | tr -s ' ' | cut -d ' ' -f 1,2 >> $CONDA_DIR/conda-meta/pinned && \
    conda clean -tipsy && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

# Install Jupyter Notebook, Lab, and Hub
# Generate a notebook server config
# Cleanup temporary files
# Correct permissions
# Do all this in a single RUN command to avoid duplicating all of the
# files across image layers when the permissions change
RUN conda install --quiet --yes \
    'notebook=5.6.*' \
    'jupyterhub=0.9.*' \
    'jupyterlab=0.34.*' && \
    conda clean -tipsy && \
    jupyter labextension install @jupyterlab/hub-extension@^0.11.0 && \
    npm cache clean --force && \
    jupyter notebook --generate-config && \
    rm -rf $CONDA_DIR/share/jupyter/lab/staging && \
    rm -rf /home/$NB_USER/.cache/yarn && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

USER root

EXPOSE 8888
WORKDIR $HOME

# Configure container startup
ENTRYPOINT ["tini", "-g", "--"]
CMD ["start-notebook.sh"]

# Add local files as late as possible to avoid cache busting
COPY start.sh /usr/local/bin/
COPY start-notebook.sh /usr/local/bin/
COPY start-singleuser.sh /usr/local/bin/
COPY jupyter_notebook_config.py /etc/jupyter/
RUN fix-permissions /etc/jupyter/

# Switch back to jovyan to avoid accidental container runs as root
USER $NB_UID

# Setup py2/3 environment
ENV PYTHON2_PATH=$CONDA_DIR/envs/python2
ENV PYTHON3_PATH=$CONDA_DIR/envs/python3

# Create user python2/3 environement
RUN conda create -n python2 python=2 ipykernel \
    && conda create -n python3 python=3 ipykernel \
    && $PYTHON2_PATH/bin/python -m ipykernel install --user \
    && $PYTHON3_PATH/bin/python -m ipykernel install --user \
    && conda clean -tipsy \
    && fix-permissions $CONDA_DIR

# Notebook/Lab dependencies,
# nbserverproxy/nbrsessionproxy is for rstudio support
# jupyter-widgets/jupyterlab-manager and matplotlib is for ipympl support which is labs
# replacement for notebook plots
RUN conda install --quiet --yes \
    'ipympl' \
    'ipyleaflet==0.9.*' \
    'nbserverproxy==0.8.*' \
    && jupyter labextension install jupyter-leaflet \
    && jupyter labextension install @jupyter-widgets/jupyterlab-manager \
    && jupyter labextension install jupyter-matplotlib \
    && npm cache clean --force \
    && rm -rf $CONDA_DIR/share/jupyter/lab/staging \
    && rm -rf /home/$NB_USER/.cache/yarn \
    && rm -rf /home/$NB_USER/.node-gyp \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Custom packages
RUN $PYTHON2_PATH/bin/pip install \
    tensorflow \
    tensorflow-gpu \
    && $PYTHON3_PATH/bin/pip install \
    tensorflow \
    tensorflow-gpu \
    && fix-permissions $CONDA_DIR

# Install facets which does not have a pip or conda package at the moment
RUN cd /tmp \
    && git clone https://github.com/PAIR-code/facets.git \
    && cd facets \
    && jupyter nbextension install facets-dist/ --sys-prefix \
    && cd \
    && rm -rf /tmp/facets \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

# Set the default python terminal links to the used kernels
# Don't delete native python3.6 -> is used by jupyter to launch the nb/lab
RUN mv $CONDA_DIR/bin/python3.6 $CONDA_DIR \
    && rm $CONDA_DIR/bin/python* \
    $CONDA_DIR/bin/pip* \
    && mv $CONDA_DIR/python3.6 $CONDA_DIR/bin/ \
    && ln -s $CONDA_DIR/bin/python3.6 $CONDA_DIR/bin/python \
    && ln -s $PYTHON2_PATH/bin/python $CONDA_DIR/bin/python2 \
    && ln -s $PYTHON3_PATH/bin/python3 $CONDA_DIR/bin/python3 \
    && ln -s $PYTHON2_PATH/bin/pip $CONDA_DIR/bin/pip \
    && ln -s $PYTHON3_PATH/bin/pip $CONDA_DIR/bin/pip3

 # Run container as
USER $NB_USER