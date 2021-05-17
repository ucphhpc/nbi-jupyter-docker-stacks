FROM nielsbohr/python-notebook:latest
LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"
ARG PACKAGE_TIMEOUT=60

USER root

RUN wget -q https://packages.microsoft.com/config/ubuntu/18.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb \
	&& dpkg -i packages-microsoft-prod.deb \
	&& apt-get update \
	&& apt-get install -yq apt-transport-https \
	&& apt-get update \
	&& apt-get install -yq dotnet-sdk-3.1 \
	&& apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER $NB_USER

RUN dotnet tool install -g Microsoft.Quantum.IQSharp \
	&& $HOME/.dotnet/tools/dotnet-iqsharp install --user

WORKDIR /home/$NB_USER

# Ensure that container Runs as
USER $NB_UID
