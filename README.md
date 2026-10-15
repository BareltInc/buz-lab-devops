# DevOps Лабораторная работа №1: Трекер арабских слов

Полный цикл разработки, контейнеризации, CI/CD и мониторинга веб-приложения.  
Проект демонстрирует сборку артефакта (wheel) в изолированном окружении, его доставку на сервер и развёртывание стека с автоматическим мониторингом.
---

## Живые ссылки

Преподавателю для проверки достаточно перейти по этим ссылкам:

| Сервис | URL | Описание |
| :--- | :--- | :--- |
| **Приложение** | [http://195.19.213.5:8080](http://195.19.213.5:8080) | Веб-интерфейс и REST API |
| **Health Check** | [http://195.19.213.5:8080/health](http://195.19.213.5:8080/health) | Статус работоспособности (JSON) |
| **Метрики (Prometheus)**| [http://195.19.213.5:8080/metrics](http://195.19.213.5:8080/metrics) | Экспорт метрик приложения |
| **Grafana** | [http://195.19.213.5:3000](http://195.19.213.5:3000) | Дашборды (логин/пароль: `admin`/`admin`) |
| **cAdvisor** | [http://195.19.213.5:8081](http://195.19.213.5:8081) | Метрики ресурсов контейнеров и хоста |

---

## Таблица соответствия требованиям

| Требование | Реализация в проекте | Файл / Директория |
| :--- | :--- | :--- |
| Веб-интерфейс и REST API (CRUD) | Flask приложение с HTML/JS фронтендом | `app/myapp/app.py`, `app/myapp/static/` |
| Сохранение данных (SQLite) | База данных вынесена в Docker Volume | `docker-compose.yml` (service: `app`) |
| Эндпоинты `/health` и `/metrics` | Реализованы, отдают JSON и формат Prometheus | `app/myapp/app.py` |
| Unit-тесты | Проверка CRUD, health и метрик | `app/tests/test_app.py` |
| Сборка артефакта в контейнере | Wheel-файл собирается внутри `python:3.12-slim` | `ci/build.sh` |
| Образ из артефакта, а не исходников | `Dockerfile` использует `ARG WHEEL_FILE` и `COPY` | `Dockerfile`, `.dockerignore` |
| Автоматический деплой | Скрипт извлекает версию и запускает compose | `deploy/deploy.sh` |
| Мониторинг (Prometheus + Grafana) | Настроен через `provisioning`, дашборд появляется сам | `monitoring/` |
| CI/CD Pipeline | GitHub Actions: тесты → артефакт → деплой по SSH | `.github/workflows/ci-cd.yml` |

---

## Процесс CI/CD 

Пайплайн запускается автоматически при `push` в ветку `main`:

1. **Build Job (Сборка)**:
   - Запускает unit-тесты внутри чистого Docker-контейнера.
   - Собирает `.whl` артефакт (wheel) также внутри контейнера.
   - Сохраняет артефакт с помощью `actions/upload-artifact`.
2. **Deploy Job (Деплой)**:
   - Скачивает артефакт из предыдущей джобы.
   - Подключается к VPS по SSH (через `appleboy/ssh-action`).
   - Передаёт артефакт на сервер и запускает `bash deploy/deploy.sh`.
   - Скрипт деплоя собирает Docker-образ **из артефакта** (не из исходников!) и перезапускает стек через `docker compose up -d --force-recreate`.

---

## Структура проекта

```text
.
├── .github/workflows/ci-cd.yml # Пайплайн GitHub Actions
├── app/                        # Исходный код приложения и тесты
│   ├── myapp/                  # Flask приложение
│   ├── tests/                  # Unit-тесты
│   └── pyproject.toml          # Метаданные пакета
├── artifacts/                  # Папка для .whl артефактов (игнорируется в git, кроме LATEST)
├── ci/                         # Скрипты сборки (build.sh, build.bat)
├── deploy/                     # Скрипты деплоя (deploy.sh, deploy.bat)
├── monitoring/                 # Конфиги Prometheus и provisioning для Grafana
├── Dockerfile                  # Инструкции для сборки образа из артефакта
├── docker-compose.yml          # Оркестрация: app, prometheus, grafana, cadvisor
└── README.md                   # Этот файл