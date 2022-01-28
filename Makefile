PATH:=$(PATH):/Users/nicolas/ets/pythonparser
PATH:=$(PATH):/Users/nicolas/ets/gumtree-3.0.0/bin
PATH:=$(PATH):/Users/nicolas/ets/jsparser

CORPUS_DIR ?= corpus
RESULTS_DIR ?= results

ALL :=

define DIFF_rule # system, file1, file2
ifneq ($(2), $(3))
$(RESULTS_DIR)/$(1)/textdiff/$(basename $(2))__$(basename $(3)).txt: $(CORPUS_DIR)/$(1)/$(2) $(CORPUS_DIR)/$(1)/$(3)
	@echo "[gumtree]  $(1): $(2) $(3)"
	@mkdir -p $$(dir $$@)
	@gumtree textdiff $$+ > $$@
ALL += $(RESULTS_DIR)/$(1)/textdiff/$(basename $(2))__$(basename $(3)).txt

$(RESULTS_DIR)/$(1)/cost/$(basename $(2))__$(basename $(3)).txt: $(RESULTS_DIR)/$(1)/textdiff/$(basename $(2))__$(basename $(3)).txt filter.py
	@echo "[cost]     $(1): $(2) $(3)"
	@mkdir -p $$(dir $$@)
	@cat $$< | python filter.py $(basename $(2)) $(basename $(3)) > $$@
ALL += $(RESULTS_DIR)/$(1)/cost/$(basename $(2))__$(basename $(3)).txt
$(RESULTS_DIR)/$(1)/costs.csv: $(RESULTS_DIR)/$(1)/cost/$(basename $(2))__$(basename $(3)).txt


$(RESULTS_DIR)/$(1)/html/$(basename $(2))__$(basename $(3)).html: $(CORPUS_DIR)/$(1)/$(2) $(CORPUS_DIR)/$(1)/$(3)
	@echo "[html]     $(1): $(2) $(3)"
	@mkdir -p $$(dir $$@)
	@diff -u $$+ | \
	diff2html --su hidden --input stdin --output stdout | \
	sed 's/<style>/<style> .d2h-file-diff{overflow-x:hidden;}/g' | \
	grep -v rtfpessoa > $$@
ALL += $(RESULTS_DIR)/$(1)/html/$(basename $(2))__$(basename $(3)).html

endif
endef

define SYSTEM_rule # system
$(foreach file1, $(shell ls $(CORPUS_DIR)/$(1)), $(foreach file2, $(shell ls $(CORPUS_DIR)/$(1)), $(eval $(call DIFF_rule,$(1),$(file1),$(file2)))))

$(RESULTS_DIR)/$(1)/costs.csv:
	@echo "[cost]     $(1)"
	@mkdir -p $$(dir $$@)
	@tail -q -n1 $$+ > $$@
ALL += $(RESULTS_DIR)/$(1)/costs.csv
endef

$(foreach system,$(shell ls $(CORPUS_DIR)),$(eval $(call SYSTEM_rule,$(system))))

clean:
	rm -rf $(RESULTS_DIR)

all: $(ALL)

