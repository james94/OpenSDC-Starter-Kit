# 28.38 MB: ubuntu 24.04
FROM ubuntu:noble

# 4.81 GB
# FROM nvidia/cuda:12.8.1-devel-ubuntu24.04

# 2.66 GB
# FROM nvidia/cuda:12.8.1-runtime-ubuntu24.04

ENV DEBIAN_FRONTEND=noninteractive

# ADD 95safe-update 94retry-get /etc/apt/apt.conf.d/

RUN apt update -y && apt install -y --no-install-recommends autoconf automake autotools-dev build-essential checkinstall curl gnupg libssl-dev libtool locales lsb-release software-properties-common vim cmake pip python-is-python3 python3 python3-dev python3-virtualenv python3-virtualenvwrapper python3-venv && apt clean

# ADD checkinstallrc /etc

RUN locale-gen en_US en_US.UTF-8

ENV export LANG en_US.UTF-8

RUN add-apt-repository -y universe

RUN add-apt-repository -y ppa:deadsnakes/ppa

RUN mkdir -p /opt/open_sdc/h-apt

# COPY apt-package-list.txt /opt/open_sdc/h-apt
# RUN apt update -y && apt install -y --no-install-recommends $(cat /opt/open_sdc/h-apt/apt-package-list.txt) && apt clean

# RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && apt update -y && apt install -y google-chrome-stable

RUN apt update -y && apt install software-properties-common apt-transport-https wget -y && wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | apt-key add - && add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" && apt install -y code

RUN python3 -m venv /opt/venv
ENV PATH "/opt/venv/bin:$PATH"

RUN pip install --upgrade pip && pip install --force-reinstall -v "conan==2.14.0" 

RUN conan profile detect
# in conan v2, conan profile update was removed, so we use sed
# RUN sed -i "s/compiler\.cppstd=.*/compiler.cppstd=gnu17/" ~/.conan2/profiles/default
# RUN sed -i "s/compiler\.libcxx=.*/compiler.libcxx=libstdc++11/" ~/.conan2/profiles/default
# RUN sed -i "s/compiler\.version=.*/compiler.version=9/" ~/.conan2/profiles/default
