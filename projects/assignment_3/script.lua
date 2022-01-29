function main(splash, args)
    splash:on_request(function(request)
        request:set_header('Accept-Language', 'en-US,en;q=0.5')
        request:set_header('user-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0')
    end)
    assert(splash:go(args.url))
    assert(splash:wait(0.5))
    return {
        html = splash:html(),
        png = splash:png(),
        har = splash:har(),
        history = splash:history()
    }
end
