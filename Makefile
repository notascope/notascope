PATH:=$(PATH):/Users/nicolas/ets/gumtree/dist/build/install/gumtree/bin
PATH:=$(PATH):/Users/nicolas/ets/tree-sitter-parser

define DIFF_rule # study, system, example, example2
ifneq ($(3), $(4))
results/$(1)/$(2)/gumtree/$(basename $(3))__$(basename $(4)).txt: studies/$(1)/$(2)/$(3) studies/$(1)/$(2)/$(4)
	@echo "[gumtree]  $(1)/$(2): $(3) $(4)"
	@mkdir -p $$(dir $$@)
	@gumtree textdiff $$+ > $$@

results/$(1)/$(2)/gumtree_cost/$(basename $(3))__$(basename $(4)).txt: results/$(1)/$(2)/gumtree/$(basename $(3))__$(basename $(4)).txt gumtree_cost.py
	@echo "[gmcost]      $(1)/$(2): $(3) $(4)"
	@mkdir -p $$(dir $$@)
	@cat $$< | python gumtree_cost.py $(1) $(2) $(basename $(3)) $(basename $(4)) > $$@
results/gumtree_costs.csv: results/$(1)/$(2)/gumtree_cost/$(basename $(3))__$(basename $(4)).txt


endif
endef

define EXAMPLE_rule # study, system, example
$(foreach example2, $(shell ls studies/$(1)/$(2)), $(eval $(call DIFF_rule,$(1),$(2),$(3),$(example2))))

results/$(1)/$(2)/source/$(basename $(3)).txt: studies/$(1)/$(2)/$(3)
	@echo "[source]   $(1)/$(2): $(3)"
	@mkdir -p $$(dir $$@)
	@cp $$< $$@
base: results/$(1)/$(2)/source/$(basename $(3)).txt

results/$(1)/$(2)/tokens/$(basename $(3)).tsv: studies/$(1)/$(2)/$(3)
	@echo "[tokens]   $(1)/$(2): $(3)"
	@mkdir -p $$(dir $$@)
	@python ts_tokenize.py $$< > $$@
results/tokens.tsv: results/$(1)/$(2)/tokens/$(basename $(3)).tsv

results/$(1)/$(2)/svg/$(basename $(3)).svg: studies/$(1)/$(2)/$(3)
	@echo "[svg]      $(1)/$(2): $(3)"
	@mkdir -p $$(dir $$@)
	@scripts/$(2).sh $$< $$@ || touch $$@
base: results/$(1)/$(2)/svg/$(basename $(3)).svg

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
