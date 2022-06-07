PATH:=$(PATH):/Users/nicolas/ets/gumtree/dist/build/install/gumtree/bin
PATH:=$(PATH):/Users/nicolas/ets/tree-sitter-parser

define DIFF_rule # study, system, example, example2
ifneq ($(3), $(4))
results/$(1)/$(2)/gumtree/$(basename $(3))__$(basename $(4)).txt: studies/$(1)/$(2)/$(3) studies/$(1)/$(2)/$(4)
	@echo "[gumtree]  $(1)/$(2): $(3) $(4)"
	@mkdir -p $$(dir $$@)
	@gumtree textdiff $$+ > $$@

results/$(1)/$(2)/cost/$(basename $(3))__$(basename $(4)).txt: results/$(1)/$(2)/gumtree/$(basename $(3))__$(basename $(4)).txt compute_costs.py
	@echo "[cost]     $(1)/$(2): $(3) $(4)"
	@mkdir -p $$(dir $$@)
	@cat $$< | python compute_costs.py $(1) $(2) $(basename $(3)) $(basename $(4)) > $$@
results/costs.csv: results/$(1)/$(2)/cost/$(basename $(3))__$(basename $(4)).txt

results/$(1)/$(2)/levenshtein/$(basename $(3))__$(basename $(4)).txt: studies/$(1)/$(2)/$(3) studies/$(1)/$(2)/$(4)
	@echo "[levensh]  $(1)/$(2): $(3) $(4)"
	@mkdir -p $$(dir $$@)
	@python levenshtein_cost.py $$+ > $$@
results/levenshtein_costs.csv: results/$(1)/$(2)/levenshtein/$(basename $(3))__$(basename $(4)).txt

results/$(1)/$(2)/unified/$(basename $(3))__$(basename $(4)).diff: studies/$(1)/$(2)/$(3) studies/$(1)/$(2)/$(4)
	@echo "[unified]  $(1)/$(2): $(3) $(4)"
	@mkdir -p $$(dir $$@)
	@diff -u $$+ > $$@ || true

results/$(1)/$(2)/html/$(basename $(3))__$(basename $(4)).html: results/$(1)/$(2)/unified/$(basename $(3))__$(basename $(4)).diff
	@echo "[html]     $(1)/$(2): $(3) $(4)"
	@mkdir -p $$(dir $$@)
	@cat $$< | \
	diff2html --su hidden --input stdin --output stdout | \
	grep -v rtfpessoa > $$@
all: results/$(1)/$(2)/html/$(basename $(3))__$(basename $(4)).html

endif
endef

define EXAMPLE_rule # study, system, example
$(foreach example2, $(shell ls studies/$(1)/$(2)), $(eval $(call DIFF_rule,$(1),$(2),$(3),$(example2))))

results/$(1)/$(2)/source/$(basename $(3)).txt: studies/$(1)/$(2)/$(3)
	@echo "[source]   $(1)/$(2): $(3)"
	@mkdir -p $$(dir $$@)
	@cp $$< $$@
all: results/$(1)/$(2)/source/$(basename $(3)).txt

results/$(1)/$(2)/tokens/$(basename $(3)).tsv: studies/$(1)/$(2)/$(3)
	@echo "[tokens]   $(1)/$(2): $(3)"
	@mkdir -p $$(dir $$@)
	@python ts_tokenize.py $$< > $$@
results/tokens.tsv: results/$(1)/$(2)/tokens/$(basename $(3)).tsv

results/$(1)/$(2)/svg/$(basename $(3)).svg: studies/$(1)/$(2)/$(3)
	@echo "[svg]      $(1)/$(2): $(3)"
	@mkdir -p $$(dir $$@)
	@scripts/$(2).sh $$< $$@ || touch $$@
all: results/$(1)/$(2)/svg/$(basename $(3)).svg

endef

define SYSTEM_rule # study, system
$(foreach example, $(shell ls studies/$(1)/$(2)), $(eval $(call EXAMPLE_rule,$(1),$(2),$(example))))
endef

define STUDY_rule # study
$(foreach system,$(shell ls studies/$(1)),$(eval $(call SYSTEM_rule,$(1),$(system))))
endef

$(foreach study,$(shell ls studies),$(eval $(call STUDY_rule,$(study))))


results/costs.csv:
	@echo "[cost]     global"
	@mkdir -p $(dir $@)
	@tail -q -n1 $+ > $@
all: results/costs.csv

results/levenshtein_costs.csv:
	@echo "[cost]     global"
	@mkdir -p $(dir $@)
	@tail -q -n1 $+ > $@
all: results/levenshtein_costs.csv

results/tokens.tsv:
	@echo "[tokens]   global"
	@mkdir -p $(dir $@)
	@cat $+ > $@
all: results/tokens.tsv

clean:
	rm -rf results

all: app.py
	touch app.py
