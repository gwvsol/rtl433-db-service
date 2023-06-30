#===========================================================
# ################## Установка приложения ##################
#===========================================================
# Установка зависимостей
.PHONY: install
install:
	@printf "\033[0m"
	@printf "\033[32m"
	@echo "================================= INSTALL VENV ================================"
	@[ -d $(VENV_NAME) ] || ${PYTHON_VERSION} -m $(VENV_NAME) $(VENV_NAME)
	@${PIP} install pip wheel -U
	@printf "\033[36m"
	@echo "============================== INSTALL VENV OK! ==============================="
	@printf "\033[0m"

# Установка зависимостей для проверки кода
.PHONY: install-dev
install-dev: ${ROBOTISK_DEPENDENCES_DEV}
	@printf "\033[0m"
	@printf "\033[32m"
	@echo "================================= INSTALL DEV ================================="
	@[ -d $(VENV_NAME) ] || ${PYTHON_VERSION} -m $(VENV_NAME) $(VENV_NAME)
	@${PIP} install pip wheel -U
	@${PIP} install -r ${RTL433DB_DEPENDENCES_DEV}
	@printf "\033[36m"
	@echo "============================== INSTALL DEV OK! ================================"
	@printf "\033[0m"

# Установка приложения RTL433DB
.PHONY: install-rtl433db
install-rtl433db: ${RTL433DB_DEPENDENCES} install
	@printf "\033[0m"
	@printf "\033[33m"
	@echo "============================== INSTALL RTL433DB ==============================="
	@${PIP} install pip wheel -U
	@${PIP} install --editable ${RTL433DB}
	@echo "============================ INSTALL RTL433DB OK! ============================="
	@printf "\033[0m"

# Активация виртуального окружения
.PHONY: venv
venv: ${VENV_NAME}/bin/activate
$(VENV_NAME)/bin/activate: ${SETUP}
	@[ -d $(VENV_NAME) ] || ${PYTHON_VERSION} -m $(VENV_NAME) $(VENV_NAME)
	@${PIP} install pip wheel -U
	@${PIP} install -e .
	@${VENV_ACTIVATE}

# Удаление виртуального окружения
.PHONY: uninstall
uninstall:
	@printf "\033[0m"
	@printf "\033[31m"
	@echo "================================= UNINSTALL ==================================="
	@make clean
	@rm -fr ${VENV_NAME}
	@printf "\033[36m"
	@echo "=============================== UNINSTALL OK! ================================="
	@printf "\033[0m"

#===========================================================
# Проверка кода
.PHONY: check
check: ${PYCODESTYLE} ${PYFLAKES} ${RTL433DB} ${RTL433DB_RUN}
	@printf "\033[0m"
	@printf "\033[32m"
	@echo "============================== CHECK SRC CODE ================================="
	@printf "\033[31m"
	@${PYCODESTYLE} ${RTL433DB}
	@${PYFLAKES} ${RTL433DB}
	@printf "\033[32m"
	@echo "============================ CHECK SRC CODE OK ================================"
	@printf "\033[0m"

#===========================================================
# Создание релиза исходного кода
.PHONY: release
release: ${RTL433DB} ${ENVIRONMENT} ${MAKEFILE} ${README} ${RTL433DB_RUN} ${COMPOSE_FILE} ${DOCKERFILE}
	@make clean
	@printf "\033[0m"
	@printf "\033[34m"
	@echo "============================ CREATE RELEASE SRC ==============================="
	@tar -cvzf ${RELEASE}/${RTL433DB}-$(EXT_NAME).tar.gz \
		${RTL433DB} ${ENVIRONMENT} ${MAKEFILE} ${README} \
		${RTL433DB_RUN} ${COMPOSE_FILE} ${DOCKERFILE}
	@printf "\033[32m"
	@printf "\nCREATE RELEASE => ${RELEASE}/${RTL433DB}-$(EXT_NAME).tar.gz\n"
	@echo "============================ CREATE RELEASE SRC OK! ==========================="
	@printf "\033[0m"

#===========================================================
# Очистка мусора
.PHONY: clean
clean:
	@printf "\033[0m"
	@printf "\033[33m"
	@echo "==================================== CLEAN ===================================="
	@[ -d $(RELEASE) ] || mkdir ${RELEASE}
	@[ -d $(ARCHIVE) ] || mkdir ${ARCHIVE}
	@find . '(' -path ./$(ARCHIVE) -o -path ./${VENV_NAME} ')' \
		-prune -o '(' -name '*.tar.gz' -o -name '*.tar.xz' -o -name '*.zip' ')' \
		-type f -exec mv -v -t "$(ARCHIVE)" {} +
	@find . '(' -path ./$(ARCHIVE) -o -path ./${VENV_NAME} ')' \
		-prune -o '(' -name '*.egg-info' -o -name '.eggs' -o -name '*~' -o -name '__pycache__' ')' \
		-exec rm -fr {} +
	@find . '(' -path ./$(ARCHIVE) -o -path ./${VENV_NAME} ')' \
		-prune -o '(' -name '*.pyc' -o -name '*.pyo' -o -name '*.spec' ')' -type f -exec rm {} +
	@printf "\033[36m"
	@echo "================================== CLEAN OK! =================================="
	@printf "\033[0m"

#===========================================================
# ############## Запуск приложения локально ################
#===========================================================

# Запуск RTL433DB
.PHONY: run
run: ${VENV_NAME} ${RTL433DB} ${RTL433DB_CLI}
	@printf "\033[0m"
	@printf "\033[33m"
	@echo "================================ RUN RTL433DB ================================="
	@printf "\033[0m"
	@${PYTHON} ${RTL433DB_CLI} run

#===========================================================
# ########### Сборка приложения RTL433DB в DOCKER ##########
#===========================================================
.PHONY: build
build: ${DOCKER} ${DOCKERFILE}
	@printf "\033[0m"
	@printf "\033[34m"
	@echo "=============================== BUILD RTL433DB ================================"
	@make release
	@printf "\033[34m"
	@${DOCKER} build \
	--file ./${DOCKERFILE} \
	--tag ${RTL433DB}:${REGISTRY_TAG} ./
#	@${DOCKER} image prune --filter label=stage=builder --force
	@printf "\033[32m"
	@echo "======================= BUILD ${RTL433DB}:${REGISTRY_TAG} ===================="
	@echo "============================ BUILD RTL433DB OK! ==============================="
	@printf "\033[0m"

#===========================================================
# ############# Публикация RTL433DB в REGISTRY #############
#===========================================================
.PHONY: deploy
deploy: clean?=
deploy: ${DOCKER}
	@printf "\033[0m"
	@printf "\033[34m"
	@echo "============================ DEPLOY IMAGE RTL433DB ============================"
	@${DOCKER} login -u ${REGISTRY_USER} -p ${REGISTRY_PASSWORD} ${REGISTRY_HOST}
	@${DOCKER} tag ${RTL433DB}:${REGISTRY_TAG} ${REGISTRY_HOST}/${RTL433DB}:${REGISTRY_TAG}
	@${DOCKER} push ${REGISTRY_HOST}/${RTL433DB}:${REGISTRY_TAG}
	@${DOCKER} rmi ${REGISTRY_HOST}/${RTL433DB}:${REGISTRY_TAG}
	@${DOCKER} logout
	@printf "\033[34m"
	@echo "========================== DEPLOY IMAGE RTL433DB OK! =========================="
	@printf "\033[32m"
	@make image clean?=${clean}
	@printf "\033[0m"

#===========================================================
# ####### Удаление локального образа DOCKER RTL433DB #######
#===========================================================

.PHONY: image
image: clean?=
image: ${DOCKER}
ifdef clean
	@printf "\033[0m"
	@printf "\033[33m"
	@echo "============================ CLEAN IMAGE RTL433DB ============================="
	@${DOCKER} rmi ${RTL433DB}:${REGISTRY_TAG}
	@echo "========================== CLEAN IMAGE RTL433DB OK ============================"
	@printf "\033[0m"
endif

#===========================================================

# Старт RTL433DB
.PHONY: start
start: ${DOCKER} ${COMPOSE_FILE}
	@${DOCKER} compose -f ${COMPOSE_FILE} up -d

# Остановка RTL433DB
.PHONY: stop
stop: ${DOCKER} ${COMPOSE_FILE}
	@${DOCKER} compose -f ${COMPOSE_FILE} down
#	@${DOCKER} container rm ${RTL433DB}

# Логирование RTL433DB
.PHONY: log
log: ${DOCKER} ${COMPOSE_FILE}
	@${DOCKER} compose -f ${COMPOSE_FILE} logs --follow --tail 500

# Рестарт RTL433DB
.PHONY: restart
restart: ${DOCKER} ${COMPOSE_FILE}
	@make stop
	@sleep 3
	@make start
