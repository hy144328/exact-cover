.PHONY: test
test:
	python3 -m pytest

.PHONY: cover
cover:
	coverage run -m pytest
	coverage report
