return {
  "Wansmer/langmapper.nvim",
  lazy = false, -- Загружать сразу, а не лениво
  priority = 1000, -- Высокий приоритет, чтобы работало до других плагинов
  config = function()
    require("langmapper").setup({
      -- Настройки по умолчанию
    })
  end,
}
