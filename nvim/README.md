# My Neovim Configuration

This is a literate configuration for Neovim. Run `make tangle` to extract the configuration files.

## Initialization

Set up the lazy package manager and load our configuration:

```lua
-- file: init.lua
-- Set up the lazy package manager
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({
    "git",
    "clone",
    "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable", -- latest stable release
    lazypath,
  })
end
vim.opt.rtp:prepend(lazypath)

-- Set lazy lua plugins and vim-options 
require("vim-options")
require("lazy").setup("plugins")

-- Set default colorscheme after plugins load
vim.cmd.colorscheme "gruvbox"
```

## Basic Vim Options

Configure basic editor settings:

```lua
-- file: lua/vim-options.lua
vim.cmd("set expandtab")
vim.cmd("set tabstop=2")
vim.cmd("set softtabstop=2")
vim.cmd("set shiftwidth=2")

vim.opt.number = true

vim.g.mapleader = " "

vim.keymap.set('n', '<leader>h', ':nohlsearch<CR>')
```

## Plugin Configuration

### Telescope

Fuzzy finder and colorscheme picker:

```lua
-- file: lua/plugins/telescope.lua
return {
  {
    "nvim-telescope/telescope-ui-select.nvim",
  },
  {
    "nvim-telescope/telescope.nvim",
    tag = "0.1.5",
    dependencies = { "nvim-lua/plenary.nvim" },
    config = function()
      require("telescope").setup({
        extensions = {
          ["ui-select"] = {
            require("telescope.themes").get_dropdown({}),
          },
        },
      })
      local builtin = require("telescope.builtin")
      vim.keymap.set("n", "<C-p>", builtin.find_files, {})
      vim.keymap.set("n", "<leader>fg", builtin.live_grep, {})
      vim.keymap.set("n", "<leader><leader>", builtin.oldfiles, {})
      vim.keymap.set("n", "<leader>cs", builtin.colorscheme, {})

      require("telescope").load_extension("ui-select")
    end,
  },
}
```

### Colorschemes

#### Catppuccin

```lua
-- file: lua/plugins/catppuccin.lua
return {
  {
    "catppuccin/nvim",
    lazy = false,
    name = "catppuccin",
    priority = 1000,
    config = true
  }
}
```

#### Gruvbox

```lua
-- file: lua/plugins/gruvbox.lua
return {
  {
    "ellisonleao/gruvbox.nvim",
    priority = 1000,
    config = true
  }
}
```

#### Tokyo Night

```lua
-- file: lua/plugins/tokyonight.lua
return {
  {
    "folke/tokyonight.nvim",
    lazy = false,
    priority = 1000,
    config = true
  }
}
```

### Neo-tree

File explorer with toggle functionality:

```lua
-- file: lua/plugins/neo-tree.lua
return {
  "nvim-neo-tree/neo-tree.nvim",
  branch = "v3.x",
  dependencies = {
    "nvim-lua/plenary.nvim",
    "nvim-tree/nvim-web-devicons",
    "MunifTanjim/nui.nvim",
  },
  config = function()
    vim.keymap.set("n", "<leader>n", ":Neotree filesystem reveal left<CR>", {})
    vim.keymap.set("n", "<leader>bf", ":Neotree buffers reveal float<CR>", {})
    vim.keymap.set("n", "<leader>nt", ":Neotree toggle<CR>", {})
  end,
}
```

### Treesitter

Syntax highlighting and parsing:

```lua
-- file: lua/plugins/treesitter.lua
return {
  "nvim-treesitter/nvim-treesitter",
  build = ":TSUpdate",
  config = function()
    local config = require("nvim-treesitter.configs")
    config.setup({
      ensure_installed = {"lua", "javascript", "c", "vim", "vimdoc"},
      highlight = { enable = true },
      indent = { enable = true },
    })
  end
}
```

### Lualine

Status line configuration:

```lua
-- file: lua/plugins/lualine.lua
return {
  'nvim-lualine/lualine.nvim',
  dependencies = { 'nvim-tree/nvim-web-devicons' },
  config = function()
    require('lualine').setup({
      options = {
        theme = 'gruvbox'
      }
    })
  end
}
```

## Usage

To regenerate configuration files from this README:

```zsh
make tangle
```

You can clean up with:

```zsh
make clean
```

To see the available options: 

```zsh
make help
```

## Keybindings

| Key                | Action                   |
|--------------------|--------------------------|
| `<leader>cs`       | Open colorscheme picker  |
| `<leader>nt`       | Toggle Neo-tree          |
| `<leader>n`        | Open Neo-tree filesystem |
| `<leader>bf`       | Open Neo-tree buffers    |
| `<C-p>`            | Find files               |
| `<leader>fg`       | Live grep                |
| `<leader><leader>` | Recent files             |
| `<leader>h`        | Clear search highlight   |
