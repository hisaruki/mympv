require 'os'

function show_playlist()
    local t = tostring(mp.get_property("playlist-pos-1")) .. "/" ..
                  tostring(mp.get_property("playlist-count"))
    mp.commandv("show_text", tostring(t))
end

mp.add_key_binding(nil, "show_playlist", function() show_playlist() end)

mp.add_key_binding(nil, "delete-confirm-and-next", function()
    local path = mp.get_property("stream-path")
    local handle = io.popen(
        'zenity --question --text "Are you sure you want to permanently delete this file?";echo $?'
    )
    local result = handle:read("*a")
    handle:close()
    result = string.gsub(result, "%s+", "")
    if result == "0" then
        mp.commandv("playlist-remove", mp.get_property("playlist-pos"))
        os.execute("rm " .. path)
        show_playlist()
    end
end)

mp.add_key_binding(nil, "trash-and-next", function()
    if not mp.get_property("audio-codec") then
        local path = mp.get_property("stream-path")
        mp.commandv("playlist-remove", mp.get_property("playlist-pos"))
        os.execute("mv " .. path .. " /tmp/")
        show_playlist()
    end
end)

mp.add_key_binding(nil, "move-and-next", function()
    if not mp.get_property("audio-codec") then
        local path = mp.get_property("stream-path")
        mp.commandv("playlist-remove", mp.get_property("playlist-pos"))
        os.execute("mv " .. path .. " ~/Pictures/2d/")
        show_playlist()
    end
end)

mp.add_key_binding(nil, "up", function()
    if mp.get_property("audio-codec") then
        mp.commandv("no-osd", "seek", "-10", "keyframes")
    else
        mp.commandv("playlist-prev")
        show_playlist()
    end
end)
mp.add_key_binding(nil, "down", function()
    if mp.get_property("audio-codec") then
        mp.commandv("no-osd", "seek", "10", "keyframes")
    else
        mp.commandv("playlist-next")
        show_playlist()
    end
end)
mp.add_key_binding(nil, "left", function()
    if mp.get_property("audio-codec") then
        mp.commandv("no-osd", "seek", "-1", "keyframes")
    else
        mp.commandv("playlist-prev")
        show_playlist()
    end
end)

mp.add_key_binding(nil, "right", function()
    if mp.get_property("audio-codec") then
        mp.commandv("no-osd", "seek", "1", "keyframes")
    else
        mp.commandv("playlist-next")
        show_playlist()
    end
end)

mp.add_key_binding(nil, "home", function()
    mp.set_property("playlist-pos-1", 1)
    show_playlist()
end)

mp.add_key_binding(nil, "end", function()
    mp.set_property("playlist-pos-1", mp.get_property("playlist-count"))
    show_playlist()
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
    local handle = io.popen(
        "sankaku -vvv --files "
        .. path
        .. " 2>&1"
    )
    local result = handle:read("*a")
    handle:close()
    mp.commandv("show_text", tostring(result), "6000")
    
end)

mp.add_key_binding(nil, "resetpan", function()
    mp.set_property("video-pan-x", 0)
    mp.set_property("video-pan-y", 0)
end)

