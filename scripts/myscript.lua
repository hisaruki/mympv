require 'os'

mp.add_key_binding (nil, "delete-confirm-and-next", function ()
    local path = mp.get_property("stream-path")
    local handle = io.popen('zenity --question --text "Are you sure you want to permanently delete this file?";echo $?')
    local result = handle:read("*a")
    handle:close()
    result = string.gsub(result, "%s+", "")
    if result == "0" then
        os.execute("rm " .. path)
        mp.command("playlist-next")        
    end
end)

mp.add_key_binding (nil, "mvtmp-and-next", function ()
    if mp.get_property("file-format").gsub(result, "%s+", "") == "mf" then
        local path = mp.get_property("stream-path")
        os.execute("mv " .. path .. " /tmp/")
        mp.command("playlist-next")
    end
end)

mp.add_key_binding (nil, "move-and-next", function ()
    if mp.get_property("file-format").gsub(result, "%s+", "") == "mf" then
        local path = mp.get_property("stream-path")
        os.execute("mv " .. path .. " ~/Pictures/2d/")
        mp.command("playlist-next")
    end
end)


mp.add_key_binding (nil, "test", function ()
    print("test")
end)
