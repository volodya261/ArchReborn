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
-- Window split
vim.keymap.set('n', '<leader>vs', ':vsp <CR>')
vim.keymap.set('n', '<leader>vp', ':sp <CR>')

-- bufferline
vim.keymap.set('n', '<leader>bd', ':bd! <CR>')
vim.keymap.set('n','<leader>bn', ':BufferLineCycleNext <CR>')
vim.keymap.set('n','<leader>bp', ':BufferLineCyclePrev <CR>')
-- comment example
vim.keymap.set('n', '<leader>bc', ':1,10s/^/#/')
--terminal
vim.keymap.set('n', '<leader>tt', ':belowright sp term://fish <CR>')
vim.keymap.set('t', '<leader>te', [[<C-\><C-n>]], { noremap = true, silent = true })

