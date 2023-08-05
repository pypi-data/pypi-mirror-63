# GitHub Webhook (micro) Framework

[![PyPI](https://img.shields.io/pypi/v/quart-github-webhook.svg)][2]

`quart-github-webhook` is a very simple, but powerful, microframework for writing [GitHub
webhooks][1] in Python. It can be used to write webhooks for individual repositories or whole
organisations, and can be used for GitHub.com or GitHub Enterprise installations; in fact, it was
orginally developed for Bloomberg's GHE install.

## Getting started

`quart-github-webhook` is designed to be as simple as possible, to make a simple Webhook that
receives push events all it takes is:

```py
from quart_github_webhook import Webhook
from quart import Quart

app = Quart(__name__)  # Standard Flask app
webhook = Webhook(app) # Defines '/postreceive' endpoint

@app.route("/")        # Standard Flask endpoint
async def hello_world():
    return "Hello, World!"

@webhook.hook()        # Defines a handler for the 'push' event
async def on_push(data):
    print("Got push with: {0}".format(data))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
```

## License

The `quart-github-webhook` repository is distributed under the Apache License (version 2.0);
see the LICENSE file at the top of the source tree for more information.

[1]: https://developer.github.com/webhooks/
[2]: https://pypi.python.org/pypi/quart-github-webhook
