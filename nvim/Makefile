# Neovim Literate Configuration Makefile

.PHONY: help tangle clean

# Default target
help: ## Show this help message
	@echo "Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

tangle: ## Extract configuration files from README.md
	@echo "Tangling configuration from README.md..."
	@lua tangle.lua

clean: ## Remove generated configuration files
	@echo "Cleaning generated configuration files..."
	@rm -f init.lua
	@rm -rf lua/
	@echo "Cleaned: init.lua and lua/ directory"
