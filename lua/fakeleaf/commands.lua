local M = {}

function M.setup()
    vim.api.nvim_create_user_command("FakeleafConnect", function(opts)
        require("fakeleaf.rpc").connect()
    end, { nargs = 0 })
end

return M
