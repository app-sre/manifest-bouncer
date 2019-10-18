TS := $(shell date '+%Y%m%d%H%M')

.PHONY: report
report:
	@./run-manifest-bouncer-saas.py

.PHONY: clone
clone:
	@rm -rf saas-repos
	@./get-saas-repos.py | ./clone-saas-repos.sh
