# ledger-cli bank importer

This is a simple cli tool to convert csv files with banking transactions into
[ledger-cli](http://ledger-cli.org/) file format.

## Similar tools

There are many tools for similar kind of job already:

 * [hledger's csv import](http://hledger.org/manual#csv-files) (haskell)
   The import feature of hledger looks nice, but it's not flexible enough for
   real banking data.
 * [CSV2Ledger](https://github.com/jwiegley/CSV2Ledger) (perl)
 * [icsv2ledger](https://github.com/quentinsf/icsv2ledger) (python) - interactive
 * [reckon](https://github.com/cantino/reckon) (ruby) - with bayesian labeling
 * [node-ledger-import](https://github.com/slashdotdash/node-ledger-import) (node.js) - inspired by reckon
 * [ledger-autosync](https://bitbucket.org/egh/ledger-autosync) (python)

All the tools (with an exception of hledger) are converting banking entries
from source (eg. csv file) into ledger file while doing additional conversions
(eg. via additional rule files, interactive prompt, bayesian labeling ...).

## Goal of this tool (ledger-bank-import)

This tools is concerned just with conversion of csv file into ledger file,
while preserving as much information as possible without additional conversions
(eg. renaming accounts, merging related csv entries into single ledger entry,
adding labels, ...), which is a job for other tools anyway.

TODO: example

## Supported source file formats

So far, we have support for:

TODO: supported file formats

## Usage

TODO: usage
