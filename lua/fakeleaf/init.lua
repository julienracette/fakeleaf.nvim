local M = {}

M.config = {
    python = "python3"
}

function M.setup(opts)
    M.config = vim.tbl_deep_extend("force", M.config, opts or {})
    require("fakeleaf.rpc").init(M.config)  -- pass config to rpc
    require("fakeleaf.commands").setup()
    print("Fakeleaf loaded")
end

return M
