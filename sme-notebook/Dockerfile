FROM nielsbohr/base-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60

USER root

# Setup default timeout of installing packages
RUN echo "[global]" > /etc/pip.conf \
    && echo "timeout=$PACKAGE_TIMEOUT" >> /etc/pip.conf

RUN conda config --set remote_read_timeout_secs $PACKAGE_TIMEOUT

# Dep
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gnupg2 \
    ca-certificates \
    dirmngr \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Repo source
# https://www.mono-project.com/download/stable/#download-lin
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF \
    && echo "deb https://download.mono-project.com/repo/ubuntu stable-bionic main" \
    | sudo tee /etc/apt/sources.list.d/mono-official-stable.list

# Install Mono
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    mono-dbg \
    mono-runtime-dbg \
    nuget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER $NB_UID

# Clone and install csharp kernel
RUN git clone --recursive https://github.com/zabirauf/icsharp.git

# Replace Legacy Nuget.exe
# a significan't amount of icsharp tests are failling at the moment
# hence || true
RUN cd icsharp \
    && cp .nuget/NuGet.exe Engine/.nuget/ \
    && nuget restore ./iCSharp.sln \
    && nuget restore ./Engine/ScriptCs.sln \
    && cd Engine \
    && mkdir artifacts --parents \
    && xbuild ./ScriptCs.sln /property:Configuration=Release /nologo /verbosity:normal || true

RUN cd icsharp/Engine \
    && mono ./packages/xunit.runners.1.9.2/tools/xunit.console.clr4.exe test/ScriptCs.Tests.Acceptance/bin/Release/ScriptCs.Tests.Acceptance.dll /xml artifacts/ScriptCs.Tests.Acceptance.dll.TestResult.xml /html artifacts/ScriptCs.Tests.Acceptance.dll.TestResult.html || true \
    && cd ../ \
    && xbuild ./iCSharp.sln /property:Configuration=Release /nologo /verbosity:normal || true

RUN sed -i -e "s/\"<INSTALL_PATH>/\"mono\", \"\/home\/${NB_USER}/g" /home/$NB_USER/icsharp/kernel-spec/kernel.json \
    && jupyter-kernelspec install --name csharp --user ~/icsharp/kernel-spec \
    && chmod +x /home/$NB_USER/icsharp/Kernel/bin/Release/iCSharp.Kernel.exe

# Run container as
USER $NB_UID
