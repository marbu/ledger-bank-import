ledger-cli bank importer
========================

This is a simple cli tool to convert csv files with banking transactions
into `ledger-cli <http://ledger-cli.org/>`__ file format. The main goal
is to preserve all information from the input file while avoiding
additional processing as much as possible.

Warning: this tools is in a initial development state and as such is
likely to not work properly on real data.

Alternatives
------------

There are many tools concerned with importing data into ledger file
format already:

-  `hledger's csv import <http://hledger.org/manual#csv-files>`__
   (haskell): The import feature of hledger looks nice, but it's not
   flexible enough for real banking data.
-  `CSV2Ledger <https://github.com/jwiegley/CSV2Ledger>`__ (perl): uses
   yaml rule files to match and label entries
-  `icsv2ledger <https://github.com/quentinsf/icsv2ledger>`__ (python):
   interactive convertion
-  `reckon <https://github.com/cantino/reckon>`__ (ruby): with bayesian
   labeling
-  `node-ledger-import <https://github.com/slashdotdash/node-ledger-import>`__
   (node.js): inspired by reckon
-  `ledger-autosync <https://bitbucket.org/egh/ledger-autosync>`__
   (python): main focus on synchronization (via ofx)

The main difference between all listed tools (with an exception of
hledger) and this project is that listed tools are converting banking
entries from source (eg. csv file) into ledger file while doing
additional conversions at the same time (eg. via additional rule files,
interactive input, bayesian labeling ...). The resulting ledger file is
expected to be directly usable without further modification.

Goal of this tool (ledger-bank-import)
--------------------------------------

This tools is concerned just with conversion of csv file into ledger
file, while preserving as much information as possible without
additional conversions (eg. renaming accounts, merging related csv
entries into single ledger entry, adding labels, ...), which is a job
for other tools anyway.

TODO: example

Supported source file formats
-----------------------------

So far, we have support for:

-  mBank.cz csv file

Usage
-----

TODO: usage
