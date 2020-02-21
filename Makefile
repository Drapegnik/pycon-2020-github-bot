.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: lint
lint:
	black .
