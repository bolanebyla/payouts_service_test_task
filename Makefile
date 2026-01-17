PYTHON := python
UV := uv
PYTHONPATH := $(shell pwd)/src
MANAGE := $(PYTHON) -m manage
PYTEST := pytest
RUFF := ruff

GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m #

help: ## Показать справку по командам
	@echo "$(GREEN)Доступные команды:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'

install: ## Установить зависимости через uv
	@echo "$(GREEN)Установка зависимостей...$(NC)"
	$(UV) pip install .

install-dev: ## Установить зависимости включая dev-зависимости
	@echo "$(GREEN)Установка зависимостей (включая dev)...$(NC)"
	$(UV) pip install . --dev

migrate: ## Применить миграции базы данных
	@echo "$(GREEN)Применение миграций...$(NC)"
	cd src && PYTHONPATH=$(PYTHONPATH) $(MANAGE) migrate

makemigrations: ## Создать новые миграции
	@echo "$(GREEN)Создание миграций...$(NC)"
	cd src && PYTHONPATH=$(PYTHONPATH) $(MANAGE) makemigrations

run: ## Запустить сервер через gunicorn
	@echo "$(GREEN)Запуск сервера через gunicorn...$(NC)"
	cd src && PYTHONPATH=$(PYTHONPATH) gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 60 --access-logfile - --error-logfile -

runserver: ## Запустить сервер разработки (runserver)
	@echo "$(GREEN)Запуск сервера разработки...$(NC)"
	cd src && PYTHONPATH=$(PYTHONPATH) $(MANAGE) runserver

worker: ## Запустить Celery worker
	@echo "$(GREEN)Запуск Celery worker...$(NC)"
	cd src && PYTHONPATH=$(PYTHONPATH) celery -A config.celery worker --pool=threads --concurrency=4 --loglevel=info --without-gossip --without-mingle --without-heartbeat

test: ## Запустить тесты
	@echo "$(GREEN)Запуск тестов...$(NC)"
	cd src && PYTHONPATH=$(PYTHONPATH) $(PYTEST)

test-verbose: ## Запустить тесты с подробным выводом
	@echo "$(GREEN)Запуск тестов с подробным выводом...$(NC)"
	cd src && PYTHONPATH=$(PYTHONPATH) $(PYTEST) -v

test-coverage: ## Запустить тесты с покрытием кода
	@echo "$(GREEN)Запуск тестов с покрытием...$(NC)"
	cd src && PYTHONPATH=$(PYTHONPATH) $(PYTEST) --cov=payouts --cov-report=html --cov-report=term

lint: ## Проверить код линтером
	@echo "$(GREEN)Проверка кода линтером...$(NC)"
	$(RUFF) check .

lint-fix: ## Автоматически исправить проблемы линтера
	@echo "$(GREEN)Автоматическое исправление проблем...$(NC)"
	$(RUFF) check --fix .

format: ## Форматировать код
	@echo "$(GREEN)Форматирование кода...$(NC)"
	$(RUFF) format .
