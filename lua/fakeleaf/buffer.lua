local M = {}
local state = require("fakeleaf.state")

function M.save_temp()
  local buf = M.ensure_buffer()
  local lines = vim.api.nvim_buf_get_lines(buf, 0, -1, false)
  local tmpfile = vim.fn.tempname() .. ".tex"
  vim.fn.writefile(lines, tmpfile)
  state.tmpfile = tmpfile
  return tmpfile
end

function M.ensure_buffer()
  if state.buf and vim.api.nvim_buf_is_valid(state.buf) then
    return state.buf
  end
  state.buf = vim.api.nvim_create_buf(false, true) -- unlisted scratch
  return state.buf
end

function M.open()
  local buf = M.ensure_buffer()
  vim.api.nvim_set_current_buf(buf)
end

function M.set_text(text)
  local buf = M.ensure_buffer()
  local lines
  if type(text) == "string" then
    lines = vim.split(text, "\n", { plain = true })
  elseif type(text) == "table" then
    lines = text
  else
    lines = { "" }
  end
  vim.api.nvim_buf_set_option(buf, "modifiable", true)
  vim.api.nvim_buf_set_lines(buf, 0, -1, false, lines)
  local tmpfile = M.save_temp()
  vim.cmd("edit " .. tmpfile)
end
return M
