#===========================================================
# Общие настройки и переменные
APPS_DIR=rtl433db
ENVIRONMENT=.env
ENVIRONMENT_APPS=.setting

# ==========================================================
VENV_NAME?=venv
VENV_BIN=${VENV_NAME}/bin
VENV_ACTIVATE=. ${VENV_BIN}/activate
PYTHON=${VENV_BIN}/python3
PIP=${VENV_BIN}/pip
# PYINSTALLER=${VENV_BIN}/pyinstaller
PYCODESTYLE=${VENV_BIN}/pycodestyle
PYFLAKES=${VENV_BIN}/pyflakes

DOCKER=$(shell which docker)

# ==========================================================

export PWD_APP=$(shell pwd)
export EXT_NAME=$(shell date '+%Y-%m-%d-%H-%M-%S')

#===========================================================

# FILE SETTING
ENVFILE_APPS=$(PWD_APP)/$(APPS_DIR)/${ENVIRONMENT_APPS}
ifneq ("$(wildcard $(ENVFILE_APPS))","")
    include ${ENVFILE_APPS}
    export ENVFILE_APPS=$(PWD_APP)/$(APPS_DIR)/${ENVIRONMENT_APPS}
endif

# ==========================================================

# FILE ENV
ENVFILE=$(PWD_APP)/${ENVIRONMENT}
ifneq ("$(wildcard $(PWD_APP)/${ENVIRONMENT})","")
    include ${ENVFILE}
    export ENVFILE=$(PWD_APP)/${ENVIRONMENT}
endif

#===========================================================

# RTL433DB
ifneq ("$(wildcard $(PWD_APP)/${APPS_DIR}/${MAKEFILE})","")
   include ${APPS_DIR}/${MAKEFILE}
endif

#===========================================================