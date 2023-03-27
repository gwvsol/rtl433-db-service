#!/bin/bash

# Скрипт для установки зависимостей

SYSTEM=$(awk -F= '$1 == "ID" { gsub(/"/, "", $NF); print($NF) }' /etc/*release)


dependents() {
echo "############################## INSTALL DEPENDENTS #############################"
if [[ "$SYSTEM" = "fedora" ]] || [[ "$SYSTEM" = "centos" ]]; then
# Установка зависимостей fedora/centos
    sudo dnf install -y automake jq gcc gcc-c++ kernel-devel libpq libpq-devel \
        git zip unzip curl wget bzip2 xz cmake autoconf rtl-433 \
        python3-devel python3-pip python3-setuptools python3-wheel
# Установка зависимостей debian
elif [[ "$SYSTEM" = "debian" ]]; then
    sudo apt-get install -y --no-install-recommends build-essential git zip unzip \
     curl wget bzip2 xz-utils cmake automake autoconf jq libpq5 libpq-dev rtl-433 \
     python3-dev python3-pip python3-setuptools python3-wheel python3-venv \
    && sudo pip3 install --upgrade wheel pip
fi

if [[ $? -ne 0 ]]; then
    echo "########################### ERROR INSTALL DEPENDENTS ##########################"
    exit 1
else
    echo "############################ INSTALL DEPENDENTS OK! ###########################"
fi
}

dependents
