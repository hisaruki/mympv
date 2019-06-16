require 'os'

mp.add_key_binding (nil, "delete-and-next", function ()
    local path = mp.get_property("stream-path")
    mp.command("playlist-next")
    os.execute("mv " .. path .. " /tmp/")
end)

mp.add_key_binding (nil, "move-and-next", function ()
    local path = mp.get_property("stream-path")
    mp.command("playlist-next")
    os.execute("mv " .. path .. " ~/Pictures/2d/")
end)