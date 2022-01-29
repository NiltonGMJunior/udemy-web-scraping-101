function main(splash, args)
    -- splash:set_user_agent("Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0")

    --[[
    headers = {
        ['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0'
    }
    splash:set_custom_headers(headers)
    --]]

    splash:on_request(function(request)
        request:set_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0')
    end)
    assert(splash:go(args.url))
    assert(splash:wait(1))
    input = assert(splash:select("input[name='q']"))
    input:focus()
    input:send_text("My user agent")
    button = splash:select_all("input[name='btnK']")
    assert(button[2].mouse_click())
    assert(splash:wait(1))
    splash:set_viewport_full()
    return {
        png = splash:png(),
        html = splash:html(),
        history = splash:history()
    }
end
