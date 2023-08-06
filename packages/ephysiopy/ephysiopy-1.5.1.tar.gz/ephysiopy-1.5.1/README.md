## Synopsis

NB THIS IS NOW OUT OF DATE AS OF 2019_10_02

Tools for the analysis of electrophysiological data collected primarily with Axona recording products using Python.

## Code Example

Main entry class is Trial contained in dacq2py_util i.e.

```
import dacq2py_util
T = dacq2py_util.Trial('/path/to/dataset/mytrial')
```

The "usual" Axona dataset includes the following files:

* mytrial.set
* mytrial.1
* mytrial.2
* mytrial.3
* mytrial.4
* mytrial.pos
* mytrial.eeg

Note that you shouldn't specify a suffix when constructing the filename in the code example above.

You can now start analysing your data! i.e.

```
T.plotEEGPower()
T.plotMap(tetrode=1, cluster=4)
```

## Motivation

Analysis using Axona's Tint cluster cutting program is great but limited. This extends that functionality.

## Installation

Easiest way is with pip (under Linux, don't know how this works under other OS's):

> pip install dacq2py

This should install all the pre-requisites, which are as follows:

* numpy
* scipy
* matplotlib
* scikits-learn
* [astropy](http://www.astropy.org/) (for NaN-friendly convolution)
* skimage
* [mahotas](http://mahotas.readthedocs.org/en/latest/)

Optional packages include:

* [klustakwik](https://github.com/klusta-team/klustakwik)

Download the files and extract to a folder and make sure it's on your Python path

## API Reference

Most classes/ methods have some explanatory text. The files in the docs folder are extracted from that using standard Python tools.

## Tests

To be implemented.

## Contributors

Robin Hayman.

## License

Do what you want license.
