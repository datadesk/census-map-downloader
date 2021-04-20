.PHONY: test ship

test:
	pipenv run flake8 ./
	pipenv run coverage run test.py
	pipenv run coverage report -m


ship:
	rm -rf build/
	rm -rf dist/
	python setup.py sdist bdist_wheel
	twine upload dist/* --skip-existing
