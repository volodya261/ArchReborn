require("config.lazy")

vim.g.mapleader = " "
vim.o.background = "dark" -- or "light" for light mode
vim.cmd([[colorscheme gruvbox]])

-- telescope
local builtin = require('telescope.builtin')
vim.keymap.set('n', '<leader>ff', builtin.find_files, { desc = 'Telescope find files' })
vim.keymap.set('n', '<leader>fg', builtin.live_grep, { desc = 'Telescope live grep' })

--treesitter
require'nvim-treesitter.configs'.setup {
  ensure_installed = { "lua","markdown", "python", "bash"},
  auto_install = true,
  ignore_install = { "javascript" },
  highlight = {
    enable = true,
    disable = { "c", "rust" },
    additional_vim_regex_highlighting = false,
  },
  ident = { enable = true },
}

-- NeoTree
vim.keymap.set('n', '<leader>e', ':Neotree filesystem reveal left<CR>')
