#===========================================================
# Общие настройки и переменные
VENV_NAME?=venv
VENV_BIN=${VENV_NAME}/bin
VENV_ACTIVATE=. ${VENV_BIN}/activate
PYTHON=${VENV_BIN}/python3
PIP=${VENV_BIN}/pip3
PYINSTALLER=${VENV_BIN}/pyinstaller
PYCODESTYLE=${VENV_BIN}/pycodestyle
PYFLAKES=${VENV_BIN}/pyflakes
export PWD_APP=$(shell pwd)

#===========================================================

ENVIRONMENT=.env
ENVFILE=$(PWD_APP)/${ENVIRONMENT}
ifneq ("$(wildcard $(PWD_APP)/${ENVIRONMENT})","")
    include ${ENVFILE}
    export ENVFILE=$(PWD_APP)/${ENVIRONMENT}
endif

#===========================================================

# RTL433DB
ifneq ("$(wildcard $(PWD_APP)/${RTL433DB}/${MAKEFILE})","")
   include ${RTL433DB}/${MAKEFILE}
endif

#===========================================================