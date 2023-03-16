define spec_rule # gallery, notation, spec

results/$(1)/$(2)/img/$(basename $(3)): galleries/$(1)/$(2)/$(3)
	@echo "[img]      $(1)/$(2): $(3)"
	@mkdir -p $$(dir $$@)
	@notations/savers/$(2).sh $$< $$@
	@touch $$@
app.py: results/$(1)/$(2)/img/$(basename $(3))

results/$(1)/$(2)/preproc/$(3): galleries/$(1)/$(2)/$(3)
	@echo "[preproc]  $(1)/$(2): $(3)"
	@mkdir -p $$(dir $$@)
	@notations/preprocessors/$(2).sh $$< $$@
	@touch $$@
results/$(1)/$(2)/distances.pqt: results/$(1)/$(2)/preproc/$(3)

results/$(1)/$(2)/pretty/$(3): galleries/$(1)/$(2)/$(3)
	@echo "[pretty]   $(1)/$(2): $(3)"
	@mkdir -p $$(dir $$@)
	@notations/prettyprinters/$(2).sh $$< $$@
	@touch $$@
app.py: results/$(1)/$(2)/pretty/$(3)

endef

define notation_rule # gallery, notation
$(foreach spec, $(shell find galleries/$(1)/$(2) -maxdepth 1 -type f ! -size 0 | sed -e 's,^.*/,,'), $(eval $(call spec_rule,$(1),$(2),$(spec))))

results/$(1)/$(2)/distances.pqt:
	@echo "[dist]     $(1)/$(2)"
	@mkdir -p $$(dir $$@)
	@python batch_distances_tokens.py results/$(1)/$(2)/preproc
results/$(1)/$(2)/tokens.pqt: results/$(1)/$(2)/distances.pqt
results/distances.pqt: results/$(1)/$(2)/distances.pqt
results/tokens.pqt: results/$(1)/$(2)/tokens.pqt

endef

define GALLERY_rule # gallery
$(foreach notation,$(shell ls galleries/$(1)),$(eval $(call notation_rule,$(1),$(notation))))


endef

$(foreach gallery,$(shell ls galleries),$(eval $(call GALLERY_rule,$(gallery))))


results/distances.pqt:
	@echo "[dist]     global"
	@mkdir -p $(dir $@)
	@python concat_pqt.py $@ $+
results/registry.json: results/distances.pqt

results/tokens.pqt:
	@echo "[tokens]   global"
	@mkdir -p $(dir $@)
	@python concat_pqt.py $@ $+
results/registry.json: results/tokens.pqt

results/registry.json:
	@echo "[registry] global"
	@python make_registry.py
app.py: results/registry.json

app.py:
	touch app.py

clean:
	rm -rf results

.PHONY: build
build: app.py
	rm -rf build
	mkdir build
	cp -r assets results src app.py notascope_components build_files/* build


.PHONY: deploy
deploy: build
	cd build && fly deploy
