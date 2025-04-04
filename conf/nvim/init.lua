require("config.lazy")
require("vim-options")

-- telescope
local builtin = require('telescope.builtin')
vim.keymap.set('n', '<leader>ff', builtin.find_files, { desc = 'Telescope find files' })
vim.keymap.set('n', '<leader>fg', builtin.live_grep, { desc = 'Telescope live grep' })

--treesitter
require'nvim-treesitter.configs'.setup {
  ensure_installed = { "lua","markdown", "python", "bash"},
  auto_install = true,
  highlight = {
    enable = true,
    additional_vim_regex_highlighting = false,
  },
  ident = { enable = true },
}

-- NeoTree
vim.keymap.set('n', '<leader>e', ':Neotree filesystem reveal left<CR>')
