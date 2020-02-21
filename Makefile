.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: lint
lint:
	black github_bot

.PHONY: start
start:
	python github_bot

.PHONY: logs
logs:
	heroku logs -a github-bots
