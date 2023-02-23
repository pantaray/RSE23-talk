# RSE23-talk
Slidedeck from my talk presenting ACME at the de-RSE 2023 conference.

## Setup

The slides were built with [Quarto](https://quarto.org/). To make the
Quarto VS Code extension (and Quarto's web server) pick up the HTML build,
first render the project

```shell
quarto render
```

Then generate a generic `index.html` by creating a symlink to the produced
`acme.html`:

```shell
ln -s acme.html index.html
```

## Publish to website

First, set `embed-resources: false` (many hosters find ~100MB html files
suspicious...), then

```shell
quarto render acme.qmd --output-dir rse23
```

Then copy the entire contents of `rse23` to the desired webspace and
check the result in a browser, e.g., www.fuertinger.science/rse23
