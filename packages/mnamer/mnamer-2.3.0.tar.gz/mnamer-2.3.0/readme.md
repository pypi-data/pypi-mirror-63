[![pypi](https://img.shields.io/pypi/v/mnamer.svg?style=for-the-badge)](https://pypi.python.org/pypi/mnamer) [![travis_ci](https://img.shields.io/travis/jkwill87/mnamer/master.svg?style=for-the-badge)](https://travis-ci.org/jkwill87/mnamer) [![coverage](https://img.shields.io/codecov/c/github/jkwill87/mnamer/master.svg?style=for-the-badge)](https://codecov.io/gh/jkwill87/mnamer) [![licence](https://img.shields.io/github/license/jkwill87/mnamer.svg?style=for-the-badge)](https://en.wikipedia.org/wiki/MIT_License) [![style black](https://img.shields.io/badge/Style-Black-black.svg?style=for-the-badge)](https://github.com/ambv/black)

![](https://github.com/jkwill87/mnamer/raw/master/assets/logo.png)

# mnamer

mnamer (**m**edia re**namer**) is an intelligent and highly configurable media organization utility. It parses media filenames for metadata, searches the web to fill in the blanks, and then renames and moves them.

Currently it has integration support with [TVDb](https://thetvdb.com) and [TvMaze](https://www.tvmaze.com) for television episodes and [TMDb](https://www.themoviedb.org/) and [OMDb](https://www.omdbapi.com) for movies.

![](https://github.com/jkwill87/mnamer/raw/master/assets/screenshot.png)

## Installation

`$ pip3 install mnamer`

## Usage

```
USAGE: mnamer [preferences] [directives] target [targets ...]

POSITIONAL:
  [TARGET,...]: media file file path(s) to process

PARAMETERS:
  The following flags can be used to customize mnamer's behaviour. Their long
  forms may also be set in a '.mnamer-v2.json' config file, in which case cli
  arguments will take precedence.

  -b, --batch: process automatically without interactive prompts
  -l, --lower: rename files using lowercase characters
  -r, --recurse: search for files within nested directories
  -s, --scene: use dots in place of alphanumeric chars
  -v, --verbose: increase output verbosity
  --hits=<NUMBER>: limit the maximum number of hits for each query
  --ignore=<PATTERN,...>: ignore files matching these regular expressions
  --mask=<EXTENSION,...>: only process given file types
  --no-cache: disable and clear request cache
  --no-guess: disable best guess; e.g. when no matches or network down
  --no-overwrite: prevent relocation if it would overwrite a file
  --no-style: print to stdout without using colour or unicode chars
  --movie-api={*tmdb,omdb}: set movie api provider
  --movie-directory: set movie relocation directory
  --movie-format: set movie renaming format specification
  --episode-api={tvdb,*tvmaze}: set episode api provider
  --episode-directory: set episode relocation directory
  --episode-format: set episode renaming format specification

DIRECTIVES:
  Directives are one-off arguments that are used to perform secondary tasks
  like overriding media detection. They can't be used in '.mnamer-v2.json'.

  -V, --version: display the running mnamer version number
  --config-dump: prints current config JSON to stdout then exits
  --config-ignore: skips loading config file for session
  --id-imdb=<ID>: specify an IMDb movie id override
  --id-tmdb=<ID>: specify a TMDb movie id override
  --id-tvdb=<ID>: specify a TVDb series id override
  --id-tvmaze=<ID>: specify a TvMaze series id override
  --media={movie,episode}: override media detection
  --test: mocks the renaming and moving of files
```

## Documentation

See mnamer's [wiki page](https://github.com/jkwill87/mnamer/wiki) for full documentation.

## Contributions

Community contributions are a welcome addition to the project. In order to be merged upsteam any additions will need to be consistent with [black](https://black.readthedocs.io) style formatting for consistency with the rest of the project and pass the continuous integration tests run against each PR. Before introducing any major features or changes to the configuration api please consider opening [an issue](https://github.com/jkwill87/mnamer/issues) to outline your proposal.

Bug reports are also welcome on the [issue page](https://github.com/jkwill87/mnamer/issues). Please include any generated crash reports if applicable. Feature requests are welcome but consider checking out [if it is in the works](https://github.com/jkwill87/mnamer/issues?q=label%3Arequest) first to avoid duplication.
