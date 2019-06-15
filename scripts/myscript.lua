require 'os'

mp.add_key_binding (nil, "delete-and-next", function ()
    local path = mp.get_property("stream-path")
    os.execute("rm " .. path)
    mp.command("playlist-next")
end)

mp.add_key_binding (nil, "move-and-next", function ()
    local path = mp.get_property("stream-path")
    os.execute("mv " .. path .. " ~/Pictures/2d/")
    mp.command("playlist-next")
end)