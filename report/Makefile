.PHONY: report
report:
	@./run-manifest-bouncer-saas.py | tee report.$(sh date '+%Y%m%d%H%M').md

.PHONY: clone
clone:
	@rm -rf saas-repos
	@./get-saas-repos.py | ./clone-saas-repos.sh
