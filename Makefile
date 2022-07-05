PATH:=$(PATH):/Users/nicolas/ets/gumtree/dist/build/install/gumtree/bin
PATH:=$(PATH):/Users/nicolas/ets/tree-sitter-parser


define EXAMPLE_rule # study, system, example

results/$(1)/$(2)/source/$(basename $(3)): studies/$(1)/$(2)/$(3)
	@echo "[source]   $(1)/$(2): $(3)"
	@mkdir -p $$(dir $$@)
	@cp $$< $$(dir $$@)
	@touch $$@
base: results/$(1)/$(2)/source/$(basename $(3))

results/$(1)/$(2)/tokens/$(basename $(3)).tsv: studies/$(1)/$(2)/$(3)
	@echo "[tokens]   $(1)/$(2): $(3)"
	@mkdir -p $$(dir $$@)
	@python ts_tokenize.py $$< > $$@
results/tokens.tsv: results/$(1)/$(2)/tokens/$(basename $(3)).tsv

results/$(1)/$(2)/img/$(basename $(3)): studies/$(1)/$(2)/$(3)
	@echo "[img]      $(1)/$(2): $(3)"
	@mkdir -p $$(dir $$@)
	@scripts/$(2).sh $$< $$@
	@touch $$@
base: results/$(1)/$(2)/img/$(basename $(3))

endef

define SYSTEM_rule # study, system
$(foreach example, $(shell ls studies/$(1)/$(2)), $(eval $(call EXAMPLE_rule,$(1),$(2),$(example))))

results/$(1)/$(2)/difflib_costs.csv:
	@echo "[difflib]  $(1)/$(2)"
	@mkdir -p $$(dir $$@)
	@python batch_difflib.py studies/$(1)/$(2)
results/difflib_costs.csv: results/$(1)/$(2)/difflib_costs.csv
endef

define STUDY_rule # study
$(foreach system,$(shell ls studies/$(1)),$(eval $(call SYSTEM_rule,$(1),$(system))))
endef

$(foreach study,$(shell ls studies),$(eval $(call STUDY_rule,$(study))))


results/gumtree_costs.csv:
	@echo "[gumtree]     global"
	@mkdir -p $(dir $@)
	@tail -q -n1 $+ > $@
gumtree: results/gumtree_costs.csv

results/difflib_costs.csv:
	@echo "[difflib]     global"
	@mkdir -p $(dir $@)
	@cat $+ > $@
difflib: results/difflib_costs.csv

results/tokens.tsv:
	@echo "[tokens]   global"
	@mkdir -p $(dir $@)
	@cat $+ > $@
base: results/tokens.tsv

clean:
	rm -rf results

base: app.py
	touch app.py
