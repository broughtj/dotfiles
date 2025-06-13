# Makefile for tangling Emacs config files

.PHONY: all clean help early-init config

# Variables
EMACS := emacs

# Default target - tangle both files
all: early config copy

# Tangle early-config.org
early:
	@echo "Tangling early-config.org..."
	@test -f early-config.org || (echo "Error: early-config.org not found" && exit 1)
	@$(EMACS) --batch --eval "(require 'org)" \
		--eval "(setq org-babel-default-header-args:emacs-lisp '((:noweb . \"yes\") (:tangle . \"early-init.el\")))" \
		--eval "(org-babel-tangle-file \"early-config.org\")"
	@echo "early-config.org tangled successfully"

# Tangle config.org  
config:
	@echo "Tangling config.org..."
	@test -f config.org || (echo "Error: config.org not found" && exit 1)
	@$(EMACS) --batch --eval "(require 'org)" \
		--eval "(setq org-babel-default-header-args:emacs-lisp '((:noweb . \"yes\") (:tangle . \"init.el\")))" \
		--eval "(org-babel-tangle-file \"config.org\")"
	@echo "config.org tangled successfully"

# Copy the early-init.el and init.el files to ~/.emacs.d/
copy:
	@echo "Copying early-init.el and init.el files..."
	@test -f early-init.el || (echo "Error: early-init.el not found" && exit 1)
	@test -f init.el || (echo "Error: init.el not found" && exit 1)
	@cp ./early-init.el ~/.emacs.d/early-init.el
	@cp ./init.el ~/.emacs.d/init.el
	@echo "early-init.el and init.el copied successfully"

# Clean up generated elisp files
clean:
	@echo "Removing generated elisp files..."
	@rm -f early-init.el init.el
	@echo "Clean complete"

# Help
help:
	@echo "Available targets:"
	@echo "  all     - Tangle both early-config.org and config.org (default)"
	@echo "  early   - Tangle early-config.org only"
	@echo "  config  - Tangle config.org only"
	@echo "  copy    - Copy generated elisp files (early-init.el, init.el) to emacs directory"
	@echo "  clean   - Remove generated elisp files (early-init.el, init.el)"
	@echo "  help    - Show this help"