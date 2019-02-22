FROM nielsbohr/slurm-notebook:latest
LABEL MAINTAINER="Mads R. B. Kristensen <madsbk@nbi.ku.dk>"

USER root

# Dep
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    cmake git unzip libboost-filesystem-dev libboost-serialization-dev libboost-regex-dev zlib1g-dev libsigsegv-dev freeglut3 freeglut3-dev libxmu-dev libxi-dev libhdf5-dev libhdf5-doc xtensor-dev xtensor-doc vim python3-h5py python3-h5py-dbg python-h5py python-h5py-dbg cgdb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --depth 5 --branch bhxx_sugar https://github.com/madsbk/bohrium.git
RUN mkdir bohrium/build
RUN cd bohrium/build && cmake .. -DVE_OPENCL=OFF -DVE_CUDA=OFF -DEXT_CLBLAS=OFF -DBRIDGE_PY_API=OFF -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=/usr && make install -j 2 \
    && cd \
    && rm -r bohrium

RUN mkdir -p /opt
RUN chgrp $NB_GID /opt
RUN chmod 774 /opt

# Launch script
RUN echo "#!/usr/bin/env bash" > /usr/local/bin/hpc_launch.sh && \
    echo "set -e" >> /usr/local/bin/hpc_launch.sh && \
    echo "git clone https://github.com/madsbk/hpc_course.git /opt/hpc_course" >> /usr/local/bin/hpc_launch.sh \
    echo "chgrp -R $NB_GID /opt/hpc_course" >> /usr/local/bin/hpc_launch.sh && \
    echo "chmod -R g+w /opt/hpc_course" >> /usr/local/bin/hpc_launch.sh \
RUN chmod a+x /usr/local/bin/hpc_launch.sh

COPY supervisord.conf /etc/supervisor/hpc-supervisord.conf
RUN cat /etc/supervisor/hpc-supervisord.conf >> /etc/supervisor/supervisord.conf \
    && rm -fr /etc/supervisor/hpc-supervisord.conf

USER $NB_USER
RUN conda install --quiet --yes ffmpeg imagemagick
RUN pip install h5py

# TODO, switch back to regular with new UID start mechanism
USER root

