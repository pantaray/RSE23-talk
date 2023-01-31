# RSE23-talk
ACME Slidedeck

## Setup

To make the Quarto VS Code extension (and Quarto's web server) pick up
the HTML build, first render the project

```shell
quarto render
```

Then generate a generic `index.html` by creating a symlink to the produced
`acme.html`:

```shell
ln -s acme.html index.html
```
