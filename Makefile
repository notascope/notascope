PATH:=$(PATH):/Users/nicolas/ets/gumtree-3.0.0/bin
#PATH:=$(PATH):/Users/nicolas/ets/gumtree/dist/build/install/gumtree/bin
#PATH:=$(PATH):/Users/nicolas/ets/jsparser
#PATH:=$(PATH):/Users/nicolas/ets/tree-sitter-parser

ALL :=
COSTS :=

define DIFF_rule # study, system, example, example2
ifneq ($(3), $(4))
results/$(1)/$(2)/gumtree/$(basename $(3))__$(basename $(4)).txt: studies/$(1)/$(2)/$(3) studies/$(1)/$(2)/$(4)
	@echo "[gumtree]  $(1)/$(2): $(3) $(4)"
	@mkdir -p $$(dir $$@)
	@gumtree -C gt.pp.path `pwd`/pythonparser textdiff $$+ > $$@

results/$(1)/$(2)/cost/$(basename $(3))__$(basename $(4)).txt: results/$(1)/$(2)/gumtree/$(basename $(3))__$(basename $(4)).txt filter.py
	@echo "[cost]     $(1)/$(2): $(3) $(4)"
	@mkdir -p $$(dir $$@)
	@cat $$< | python filter.py $(1) $(2) $(basename $(3)) $(basename $(4)) > $$@
results/$(1)/$(2)/costs.csv: results/$(1)/$(2)/cost/$(basename $(3))__$(basename $(4)).txt

results/$(1)/$(2)/unified/$(basename $(3))__$(basename $(4)).diff: studies/$(1)/$(2)/$(3) studies/$(1)/$(2)/$(4)
	@echo "[unified]   $(1)/$(2): $(3) $(4)"
	@mkdir -p $$(dir $$@)
	@diff -u $$+ > $$@ || true

results/$(1)/$(2)/html/$(basename $(3))__$(basename $(4)).html: results/$(1)/$(2)/unified/$(basename $(3))__$(basename $(4)).diff
	@echo "[html]     $(1)/$(2): $(3) $(4)"
	@mkdir -p $$(dir $$@)
	@cat $$< | \
	diff2html --su hidden --input stdin --output stdout | \
	sed 's/<style>/<style> .d2h-file-diff{overflow-x:hidden;}/g' | \
	grep -v rtfpessoa > $$@
ALL += results/$(1)/$(2)/html/$(basename $(3))__$(basename $(4)).html

endif
endef

define EXAMPLE_rule # study, system, example
$(foreach example2, $(shell ls studies/$(1)/$(2)), $(eval $(call DIFF_rule,$(1),$(2),$(3),$(example2))))

results/$(1)/$(2)/source/$(basename $(3)).txt: studies/$(1)/$(2)/$(3)
	@echo "[source]   $(1)/$(2): $(3)"
	@mkdir -p $$(dir $$@)
	@cp $$< $$@
ALL += results/$(1)/$(2)/source/$(basename $(3)).txt

results/$(1)/$(2)/png/$(basename $(3)).png: studies/$(1)/$(2)/$(3)
	@echo "[png]      $(1)/$(2): $(3)"
	@mkdir -p $$(dir $$@)
	@scripts/$(2).sh $$< $$@
ALL += results/$(1)/$(2)/png/$(basename $(3)).png

endef

define SYSTEM_rule # study, system
$(foreach example, $(shell ls studies/$(1)/$(2)), $(eval $(call EXAMPLE_rule,$(1),$(2),$(example))))

results/$(1)/$(2)/costs.csv:
	@echo "[cost]     $(1)/$(2)"
	@mkdir -p $$(dir $$@)
	@tail -q -n1 $$+ > $$@
results/$(1)/costs.csv: results/$(1)/$(2)/costs.csv
endef

define STUDY_rule # study
$(foreach system,$(shell ls studies/$(1)),$(eval $(call SYSTEM_rule,$(1),$(system))))

results/$(1)/costs.csv:
	@echo "[cost]     all"
	@mkdir -p $$(dir $$@)
	@cat $$+ > $$@
ALL += results/$(1)/costs.csv
endef

$(foreach study,$(shell ls studies),$(eval $(call STUDY_rule,$(study))))

clean:
	rm -rf results

all: $(ALL)

reload: all
	touch app.py
