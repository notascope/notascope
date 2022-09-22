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
	@savers/$(2).sh $$< $$@
	@touch $$@
base: results/$(1)/$(2)/img/$(basename $(3))

results/$(1)/$(2)/preproc/$(3): studies/$(1)/$(2)/$(3)
	@echo "[preproc]  $(1)/$(2): $(3)"
	@mkdir -p $$(dir $$@)
	@preprocessors/$(2).sh $$< $$@
	@touch $$@
results/$(1)/$(2)/difflib_costs.csv results/$(1)/$(2)/ncd_costs.csv: results/$(1)/$(2)/preproc/$(3)

endef

define SYSTEM_rule # study, system
$(foreach example, $(shell find studies/$(1)/$(2) -maxdepth 1 -type f ! -size 0 | sed -e 's,^.*/,,'), $(eval $(call EXAMPLE_rule,$(1),$(2),$(example))))

results/$(1)/$(2)/difflib_costs.csv:
	@echo "[difflib]  $(1)/$(2)"
	@mkdir -p $$(dir $$@)
	@python batch_difflib.py results/$(1)/$(2)/preproc
results/difflib_costs.csv: results/$(1)/$(2)/difflib_costs.csv


results/$(1)/$(2)/ncd_costs.csv:
	@echo "[ncd]      $(1)/$(2)"
	@mkdir -p $$(dir $$@)
	@python batch_ncd.py results/$(1)/$(2)/preproc
results/ncd_costs.csv: results/$(1)/$(2)/ncd_costs.csv
endef

define STUDY_rule # study
$(foreach system,$(shell ls studies/$(1)),$(eval $(call SYSTEM_rule,$(1),$(system))))
endef

$(foreach study,$(shell ls studies),$(eval $(call STUDY_rule,$(study))))


results/difflib_costs.csv:
	@echo "[difflib]  global"
	@mkdir -p $(dir $@)
	@cat $+ > $@
difflib: results/difflib_costs.csv

results/ncd_costs.csv:
	@echo "[ncd]      global"
	@mkdir -p $(dir $@)
	@cat $+ > $@
ncd: results/ncd_costs.csv

results/tokens.tsv:
	@echo "[tokens]   global"
	@mkdir -p $(dir $@)
	@cat $+ > $@
base: results/tokens.tsv

clean:
	rm -rf results

base: app.py
	python make_html.py
	touch app.py
