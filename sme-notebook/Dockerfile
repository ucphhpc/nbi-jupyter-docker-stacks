FROM nielsbohr/base-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60

USER root

# Setup default timeout of installing packages
RUN echo "[global]" > /etc/pip.conf \
    && echo "timeout=$PACKAGE_TIMEOUT" >> /etc/pip.conf

# Dep
# https://www.mono-project.com/download/stable/#download-lin
# Install Mono
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gnupg2 \
    ca-certificates \
    dirmngr \
    && apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF \
    && echo "deb https://download.mono-project.com/repo/ubuntu stable-bionic main" \
    | sudo tee /etc/apt/sources.list.d/mono-official-stable.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    mono-devel \
    mono-complete \
    mono-dbg \
    nuget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp

USER $NB_UID

RUN conda config --set remote_read_timeout_secs $PACKAGE_TIMEOUT \
    && mkdir -p /home/$NB_USER/.local/bin/icsharp

# Clone and install csharp kernel
# Replace Legacy Nuget.exe
# a significan't amount of icsharp tests are failling at the moment
# hence || true
RUN git clone --recursive https://github.com/zabirauf/icsharp.git \
    && cd icsharp \
    && git checkout 333f651c610ed1b96e227cc93e8b69d7d303134f \
    && nuget restore ./iCSharp.sln \
    && nuget restore ./Engine/ScriptCs.sln \
    && cd Engine \
    && mkdir artifacts --parents \
    && xbuild ./ScriptCs.sln /property:Configuration=Release /nologo /verbosity:normal \
    && mono ./packages/xunit.runners.1.9.2/tools/xunit.console.clr4.exe test/ScriptCs.Tests.Acceptance/bin/Release/ScriptCs.Tests.Acceptance.dll /xml artifacts/ScriptCs.Tests.Acceptance.dll.TestResult.xml /html artifacts/ScriptCs.Tests.Acceptance.dll.TestResult.html || true \
    && cd ../ \
    && xbuild ./iCSharp.sln /property:Configuration=Release /nologo /verbosity:normal \
    && sed -i -e "s/\"<INSTALL_PATH>\/icsharp\/Kernel\/bin\/Release/\"mono\", \"\/home\/${NB_USER}\/.local\/bin\/icsharp/g" /tmp/icsharp/kernel-spec/kernel.json \
    && jupyter-kernelspec install --name csharp --user /tmp/icsharp/kernel-spec \
    && cp -r /tmp/icsharp/Kernel/bin/Release/* /home/$NB_USER/.local/bin/icsharp/ \
    && chmod +x /home/$NB_USER/.local/bin/icsharp/iCSharp.Kernel.exe \
    && rm -fr /tmp/icsharp \
    && fix-permissions $CONDA_DIR \
    && fix-permissions /home/$NB_USER

USER root

RUN echo "PATH=\"/home/$NB_USER/.local/bin:$PATH\"" >> /home/$NB_USER/.bashrc

WORKDIR /home/$NB_USER

# Ensure that container Runs as
USER $NB_UID
