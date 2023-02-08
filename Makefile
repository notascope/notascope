define spec_rule # gallery, notation, spec

results/$(1)/$(2)/source/$(basename $(3)): galleries/$(1)/$(2)/$(3)
	@echo "[source]   $(1)/$(2): $(3)"
	@mkdir -p $$(dir $$@)
	@cp $$< $$(dir $$@)
	@touch $$@
all: results/$(1)/$(2)/source/$(basename $(3))

results/$(1)/$(2)/img/$(basename $(3)): galleries/$(1)/$(2)/$(3)
	@echo "[img]      $(1)/$(2): $(3)"
	@mkdir -p $$(dir $$@)
	@notations/savers/$(2).sh $$< $$@
	@touch $$@
all: results/$(1)/$(2)/img/$(basename $(3))

results/$(1)/$(2)/preproc/$(3): galleries/$(1)/$(2)/$(3)
	@echo "[preproc]  $(1)/$(2): $(3)"
	@mkdir -p $$(dir $$@)
	@notations/preprocessors/$(2).sh $$< $$@
	@touch $$@
results/$(1)/$(2)/difflib_costs.csv results/$(1)/$(2)/ncd_costs.csv results/$(1)/$(2)/tokens.tsv: results/$(1)/$(2)/preproc/$(3)

results/$(1)/$(2)/pretty/$(3): galleries/$(1)/$(2)/$(3)
	@echo "[pretty]   $(1)/$(2): $(3)"
	@mkdir -p $$(dir $$@)
	@notations/prettyprinters/$(2).sh $$< $$@
	@touch $$@
all: results/$(1)/$(2)/pretty/$(3)

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


endef

$(foreach gallery,$(shell ls galleries),$(eval $(call GALLERY_rule,$(gallery))))


results/difflib_costs.csv:
	@echo "[difflib]  global"
	@mkdir -p $(dir $@)
	@cat $+ > $@
all: results/difflib_costs.csv

results/ncd_costs.csv:
	@echo "[ncd]      global"
	@mkdir -p $(dir $@)
	@cat $+ > $@
all: results/ncd_costs.csv

results/tokens.tsv:
	@echo "[tokens]   global"
	@mkdir -p $(dir $@)
	@cat $+ > $@
all: results/tokens.tsv

results/registry.json: all
	@echo "[registry] global"
	@python make_registry.py

app.py: results/registry.json
	touch app.py

clean:
	rm -rf results
