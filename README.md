# Git Hooks for PHP / JS / Less / Sass / CSS project

## Why?

To automatize basic code linting and quality checking on commit.

## What does it do?

It runs some basic linters when you commit files.

#### PHP

- Looks for dump, die, dd, print_r statements in the staged files
- Checks the staged code syntax with PHPCS (optional, if PHPCS is present)

#### JavaScript

- Looks for `console.log` or `debugger` in the staged files
- Checks the staged code's syntax with JSHint (optional, if JSHint is present)


#### StyleSheets (Less, Sass, CSS, HTML)

- Checks the staged code with StyleLint

## Installation

Create the destination directory and enter it:
```bash
mkdir "$HOME/.git-hooks" && cd "$_"
```

Download the repository's content and unzip in the current dir:

With wget
```bash
wget -c https://github.com/GuillaumeSMedia/git-hooks/archive/master.tar.gz -O - | tar -xz --strip 1
```

or with curl:
```bash
curl -L -s https://github.com/GuillaumeSMedia/git-hooks/archive/master.tar.gz | tar -xz --strip 1
```

Change the default global git hooks directory to the current dir:

```bash
git config --global core.hooksPath $PWD
```

## Use

Simply cd into a local git repository and commit some files (PHP, JS, SASS, LESS, CSS and/or HTML).

## Troubleshooting

Use the `-n` flag with `git commit` to skip the checks if necessary.

## Todo / Ideas

- [X] Add basic documentation
- [ ] Allow local (per project) config override
- [ ] Implement additional plugins

## Resources

- Git Hooks documentation: https://git-scm.com/book/uz/v2/Customizing-Git-Git-Hooks
- PHPCS: https://github.com/squizlabs/PHP_CodeSniffer
- JSHint: https://jshint.com/docs/
- StyleLint: https://stylelint.io/

## Contribute

Pull requests are welcome :)