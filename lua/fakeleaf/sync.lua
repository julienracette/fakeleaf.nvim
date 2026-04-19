local M = {}
local rpc = require("fakeleaf.rpc")

local pickers = require("telescope.pickers")
local finders = require("telescope.finders")
local conf = require("telescope.config").values
local actions = require("telescope.actions")
local action_state = require("telescope.actions.state")

local json = vim.json
local function reverse_dict(dict)
    local reversed = {}
    for k, v in pairs(dict) do
        reversed[v] = k
    end
    return reversed
end
local function pick_from_dict(dict, callback)
    local items = {}
    for k, v in pairs(dict) do
        table.insert(items, { key = k, value = v, display = k .. ": " .. tostring(v) })
    end

    pickers.new({}, {
        prompt_title = "Pick item",
        finder = finders.new_table({
            results = items,
            entry_maker = function(entry)
                return {
                    value = entry,
                    display = entry.display,
                    ordinal = entry.display,
                }
            end,
        }),
        sorter = conf.generic_sorter({}),
        attach_mappings = function(prompt_bufnr, _)
            actions.select_default:replace(function()
                actions.close(prompt_bufnr)
                local selection = action_state.get_selected_entry()
                callback(selection.value)
            end)
            return true
        end,
    }):find()
end


function M.handle(msg)
    if msg.type == "full_text" then
        require("fakeleaf.buffer").set_text(msg.content)
    
    elseif msg.type == "projects_dict" then
        local projects_dict = json.decode(msg.content)
        local selected
        pick_from_dict(reverse_dict(projects_dict),function(item)
            selected = item.value
            rpc.send(
            {
                type = "connect",
                id = selected
            })

        end)

    elseif msg.type == "sendfile" then
        require("fakeleaf.buffer").set_text(msg.lines)

    elseif msg.type == "doc_ids" then 

        vim.cmd("NvimTreeClose")
        local tmpdir = vim.fn.tempname()
        vim.fn.mkdir(tmpdir, "p")
        for _, name in pairs(msg.list) do
            vim.fn.writefile({_}, tmpdir .. "/" .. name)
        end
        vim.cmd("cd " .. tmpdir)
        vim.cmd("NvimTreeOpen" .. tmpdir)
    elseif msg.type == "error" then
        vim.notify(msg.message, vim.log.levels.ERROR)
    elseif msg.type =="debug" then
        print("Debug:",msg.message)

    else
        print("Unknown message:", vim.inspect(msg))
    end
end

return M
