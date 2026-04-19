local M = {}
local state = require("fakeleaf.state")


function M.init(opts)
    config = opts or {}
end

function M.start()
    if state.job_id then
        return
    end
    local python = config.python or python
    state.job_id = vim.fn.jobstart(

        {python,"-m", "fakeleaf_bridge" }, {
        on_stdout = function(_, data)
            for _, line in ipairs(data) do
                if line ~= "" then
                    local ok, msg = pcall(vim.json.decode, line)
                    if ok then
                        require("fakeleaf.sync").handle(msg)
                    else
                        vim.notify("Invalid JSON: " .. line, vim.log.levels.ERROR)
                    end
                end
            end
        end,

        on_stderr = function(_, data)
            for _, line in ipairs(data) do
                if line ~= "" then
                    vim.notify("Bridge stderr: " .. line, vim.log.levels.WARN)
                end
            end
        end,
    })
end

function M.send(msg)
    if not state.job_id then
        vim.notify("Bridge not started", vim.log.levels.ERROR)
        return
    end
    vim.fn.chansend(state.job_id, vim.json.encode(msg) .. "\n")
end

function M.connect()
    M.start()

    M.send({
        type = "fetch",
    })
end
return M
