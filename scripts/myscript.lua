require 'os'
require 'io'


function show_playlist()
    local t = tostring(mp.get_property("playlist-pos-1"))
    t = t  .. "/" .. tostring(mp.get_property("playlist-count"))
    mp.commandv("show_text", tostring(t))
end

mp.add_key_binding(nil, "show_playlist", function() show_playlist() end)

mp.add_key_binding(nil, "delete-confirm-and-next", function()
    local path = mp.get_property("stream-path")
    os.execute("python3 command.py delete-confirm-next " .. path)
end)

mp.add_key_binding(nil, "delete-and-next", function()
    local path = mp.get_property("stream-path")
    os.execute("python3 command.py delete-and-next " .. path)
end)

mp.add_key_binding(nil, "move-and-next", function()
    local path = mp.get_property("stream-path")
    os.execute("python3 command.py move-and-next " .. path)
end)

mp.add_key_binding(nil, "copy-desktop", function()
    local path = mp.get_property("stream-path")
    os.execute("python3 command.py copy-desktop " .. path)
end)

mp.add_key_binding(nil, "up", function()
    if mp.get_property("audio-codec") then
        mp.commandv("osd-bar", "seek", "-3", "relative-percent+exact")
    else
        mp.commandv("playlist-prev")
        show_playlist()
    end
end)
mp.add_key_binding(nil, "down", function()
    if mp.get_property("audio-codec") then
        mp.commandv("osd-bar", "seek", "3", "relative-percent+exact")
    else
        mp.commandv("playlist-next")
        show_playlist()
    end
end)
mp.add_key_binding(nil, "left", function()
    if mp.get_property("audio-codec") then
        mp.commandv("no-osd", "seek", "-10", "keyframes")
    else
        mp.commandv("playlist-prev")
        show_playlist()
    end
end)

mp.add_key_binding(nil, "right", function()
    if mp.get_property("audio-codec") then
        mp.commandv("no-osd", "seek", "10", "keyframes")
    else
        mp.commandv("playlist-next")
        show_playlist()
    end
end)

mp.add_key_binding(nil, "home", function()
    mp.set_property("playlist-pos-1", 1)
end)

mp.add_key_binding(nil, "end", function()
    mp.set_property("playlist-pos-1", mp.get_property("playlist-count"))
end)

mp.add_key_binding(nil, "rotate", function()
    local v = mp.get_property("options/video-rotate")
    v = v + 90
    if v >= 360 then
      v = v - 360
    end
    mp.set_property("options/video-rotate", v)

end)

mp.add_key_binding(nil, "info", function()
    local path = mp.get_property("stream-path")
    local result = tostring(path)
    mp.commandv("show_text", tostring(result), "6000")
    
end)

mp.add_key_binding(nil, "resetpan", function()
    mp.set_property("video-pan-x", 0)
    mp.set_property("video-pan-y", 0)
end)

