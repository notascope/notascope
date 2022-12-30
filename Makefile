PATH:=$(PATH):/Users/nicolas/ets/tree-sitter-parser


define spec_rule # gallery, notation, spec

results/$(1)/$(2)/source/$(basename $(3)): galleries/$(1)/$(2)/$(3)
	@echo "[source]   $(1)/$(2): $(3)"
	@mkdir -p $$(dir $$@)
	@cp $$< $$(dir $$@)
	@touch $$@
base: results/$(1)/$(2)/source/$(basename $(3))

results/$(1)/$(2)/img/$(basename $(3)): galleries/$(1)/$(2)/$(3)
	@echo "[img]      $(1)/$(2): $(3)"
	@mkdir -p $$(dir $$@)
	@savers/$(2).sh $$< $$@
	@touch $$@
base: results/$(1)/$(2)/img/$(basename $(3))
results/$(1)/summary.html: results/$(1)/$(2)/img/$(basename $(3))

results/$(1)/$(2)/preproc/$(3): galleries/$(1)/$(2)/$(3)
	@echo "[preproc]  $(1)/$(2): $(3)"
	@mkdir -p $$(dir $$@)
	@preprocessors/$(2).sh $$< $$@
	@touch $$@
results/$(1)/$(2)/difflib_costs.csv results/$(1)/$(2)/ncd_costs.csv results/$(1)/$(2)/tokens.tsv: results/$(1)/$(2)/preproc/$(3)

results/$(1)/$(2)/pretty/$(3): galleries/$(1)/$(2)/$(3)
	@echo "[pretty]   $(1)/$(2): $(3)"
	@mkdir -p $$(dir $$@)
	@prettyprinters/$(2).sh $$< $$@
	@touch $$@
base: results/$(1)/$(2)/pretty/$(3)

endef

define notation_rule # gallery, notation
$(foreach spec, $(shell find galleries/$(1)/$(2) -maxdepth 1 -type f ! -size 0 | sed -e 's,^.*/,,'), $(eval $(call spec_rule,$(1),$(2),$(spec))))

results/$(1)/$(2)/difflib_costs.csv:
	@echo "[difflib]  $(1)/$(2)"
	@mkdir -p $$(dir $$@)
	@python batch_difflib.py results/$(1)/$(2)/preproc
results/$(1)/$(2)/tokens.tsv: results/$(1)/$(2)/difflib_costs.csv
results/difflib_costs.csv: results/$(1)/$(2)/difflib_costs.csv
results/tokens.tsv: results/$(1)/$(2)/tokens.tsv


results/$(1)/$(2)/ncd_costs.csv:
	@echo "[ncd]      $(1)/$(2)"
	@mkdir -p $$(dir $$@)
	@python batch_ncd.py results/$(1)/$(2)/preproc
results/ncd_costs.csv: results/$(1)/$(2)/ncd_costs.csv
endef

define GALLERY_rule # gallery
$(foreach notation,$(shell ls galleries/$(1)),$(eval $(call notation_rule,$(1),$(notation))))


results/$(1)/summary.html:
	@echo "[summary]  $(1)"
	@mkdir -p $$(dir $$@)
	@python make_html.py $(1)
base: results/$(1)/summary.html

endef

$(foreach gallery,$(shell ls galleries),$(eval $(call GALLERY_rule,$(gallery))))


results/difflib_costs.csv:
	@echo "[difflib]  global"
	@mkdir -p $(dir $@)
	@cat $+ > $@
base: results/difflib_costs.csv

results/ncd_costs.csv:
	@echo "[ncd]      global"
	@mkdir -p $(dir $@)
	@cat $+ > $@
ncd: results/ncd_costs.csv

results/tokens.tsv:
	@echo "[tokens]   global"
	@mkdir -p $(dir $@)
	@cat $+ > $@

results/registry.json: results/tokens.tsv
	@echo "[registry] global"
	@python make_registry.py
base: results/registry.json


clean:
	rm -rf results

base ncd: app.py
	touch app.py
