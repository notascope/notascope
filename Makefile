PATH:=$(PATH):/Users/nicolas/ets/pythonparser
PATH:=$(PATH):/Users/nicolas/ets/gumtree-3.0.0/bin
PATH:=$(PATH):/Users/nicolas/ets/jsparser


ALL :=

define DIFF_rule # system, example, example2
ifneq ($(2), $(3))
results/$(1)/textdiff/$(basename $(2))__$(basename $(3)).txt: corpus/$(1)/$(2) corpus/$(1)/$(3)
	@echo "[gumtree]  $(1): $(2) $(3)"
	@mkdir -p $$(dir $$@)
	@gumtree textdiff $$+ > $$@
ALL += results/$(1)/textdiff/$(basename $(2))__$(basename $(3)).txt

results/$(1)/cost/$(basename $(2))__$(basename $(3)).txt: results/$(1)/textdiff/$(basename $(2))__$(basename $(3)).txt filter.py
	@echo "[cost]     $(1): $(2) $(3)"
	@mkdir -p $$(dir $$@)
	@cat $$< | python filter.py $(basename $(2)) $(basename $(3)) > $$@
results/$(1)/costs.csv: results/$(1)/cost/$(basename $(2))__$(basename $(3)).txt


results/$(1)/html/$(basename $(2))__$(basename $(3)).html: corpus/$(1)/$(2) corpus/$(1)/$(3)
	@echo "[html]     $(1): $(2) $(3)"
	@mkdir -p $$(dir $$@)
	@diff -u $$+ | \
	diff2html --su hidden --input stdin --output stdout | \
	sed 's/<style>/<style> .d2h-file-diff{overflow-x:hidden;}/g' | \
	grep -v rtfpessoa > $$@
ALL += results/$(1)/html/$(basename $(2))__$(basename $(3)).html

endif
endef

define EXAMPLE_rule # system, example
$(foreach example2, $(shell ls corpus/$(1)), $(eval $(call DIFF_rule,$(1),$(2),$(example2))))


results/$(1)/png/$(basename $(2)).png: corpus/$(1)/$(2)
	@echo "[png]      $(1): $(2)"
	@mkdir -p $$(dir $$@)
	@scripts/$(1)/save.sh $$< $$@
ALL += results/$(1)/png/$(basename $(2)).png

endef

define SYSTEM_rule # system
$(foreach example, $(shell ls corpus/$(1)), $(eval $(call EXAMPLE_rule,$(1),$(example))))

results/$(1)/costs.csv:
	@echo "[cost]     $(1)"
	@mkdir -p $$(dir $$@)
	@tail -q -n1 $$+ > $$@
ALL += results/$(1)/costs.csv
endef

$(foreach system,$(shell ls corpus),$(eval $(call SYSTEM_rule,$(system))))

clean:
	rm -rf results

all: $(ALL)

