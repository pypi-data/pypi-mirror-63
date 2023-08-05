## The Local News

Get the local news on your cli about the any topic

### Install
====================

```bash
pip install news-cli

Usage: news [OPTIONS]
  Read news on your command line.

Options:
  --area    TEXT  Area of interest  [default: USA]
  --keyword TEXT  Specific news for the keyword
  --help          Show this message and exit.

```

![](resources/news-cli_v2.gif)


### Run
====================

```javascript

news # displays top news from US
news --area technology # display tech news
news --keyword coronavirus # show news about coronavirus keyword
news --url  # open url for first news item
news --area india --url  4 # open url for 4th item on the list

```

### Developers
====================

1. Create wheel file using command
    `python setup.py bdist_wheel`
2. A `*.whl` file is generated inside dist folder
3. Use `pip install *.whl` to install the CLI