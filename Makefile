prepare:
	python serv/manage.py compass
	python serv/manage.py collectstatic --noinput

tagn="$(shell cat release)"
tag:
	git tag -a $(tagn) -m "add tag $(tagn)"
	git push --tags

params: tag
params:
	@echo "PROJECT=sancta_serv\nTAG=$(tagn)" > project.params


