return {
	"rebelot/kanagawa.nvim",
	config = function()
		require('kanagawa').setup({
			compile = true,
			transparent = true,
			theme = "lotus",
			background = {
				dark = "wave",
				light = "lotus"
			},
		});
		vim.cmd("colorscheme kanagawa");
	end,
	build = function()
		vim.cmd("KanagawaCompile");
	end,
}

