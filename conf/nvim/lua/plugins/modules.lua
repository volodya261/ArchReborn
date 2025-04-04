return {
 {
    'windwp/nvim-autopairs',
    event = "InsertEnter",
    config = true
 },

 { "ellisonleao/gruvbox.nvim", priority = 1000 , config = true, opts = ...},

 {
     'nvim-telescope/telescope.nvim',
      dependencies = { 'nvim-lua/plenary.nvim' }
 },

 {"nvim-treesitter/nvim-treesitter", build = ":TSUpdate"},

 {
  "nvim-neo-tree/neo-tree.nvim",
  dependencies = {
    "nvim-lua/plenary.nvim",
    "nvim-tree/nvim-web-devicons", 
    "MunifTanjim/nui.nvim",
  },
 },

 {
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
    
}
