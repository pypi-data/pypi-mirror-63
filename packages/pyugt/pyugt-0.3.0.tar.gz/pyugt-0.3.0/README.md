# pyugt - Python Universal Game Translator

[![PyPI-Status](https://img.shields.io/pypi/v/pyugt.svg)](https://pypi.org/project/pyugt)
[![PyPI-Versions](https://img.shields.io/pypi/pyversions/pyugt.svg?logo=python&logoColor=white)](https://pypi.org/project/pyugt)
[![PyPI-Downloads](https://img.shields.io/pypi/dm/pyugt.svg?logo=python&logoColor=white)](https://pypi.org/project/pyugt)

pyugt is a python universal game translator: it takes screenshots from a region you select on your screen, uses OCR (via Tesseract v5) to extract the characters, then feeds them to a machine translator (Google Translate) to then show you a translated text.

Since it works directly on images, there is no need to hack the game or anything to access the text. It is also cross-platform (support for Windows and Linux - MacOSX does not yet work because hotkeys are not supported on this platform for now).

Here is a demo:
![demo](https://github.com/lrq3000/pyugt/raw/master/doc/demo.gif)

Of course, since the translation is done by a machine, don't expect a very nice translation, but for games where no translation is available, it can be sufficient to understand the gist and be able to play.

This software was inspired by the amazing work of Seth Robinson on [UGT (Universal Game Translator)](https://github.com/SethRobinson/UGT).

## How to install & update

First, install Tesseract v5, installers are provided by [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki). Make sure to install the additional languages you want to translate from (eg, Japanese).

Also, you need to install a Python interpreter. [Anaconda](https://www.anaconda.com/distribution/) is a good one.

Then, install this software:

`pip install --upgrade pyugt`

Or maybe what can be more easy if you want to edit the config file, is to download the archive from Github, unzip anywhere, cd in the folder and type:

`python setup.py develop`

Note the software was tested on Windows 10 x64 with Python 3.7 (Anaconda). It should also work on other Python versions and on Linux but this was not tested (please let me know if you try on Linux!).

## How to use

* First, you need to configure the config file `config.ini`. A sample config file is provided with the software that should work fine on Windows, but on other platforms or in some cases you may need to edit it, particularly to setup the path to the Tesseract binaries.
  The config file also allows you to change the hotkeys and the monitor to screenshot from, and a few other things such as the source and target languages (by default, the source is japanese and target is english).

* Then, you can launch the script from a terminal/console:

`pyugt`

or:

`python -m pyugt`

* Then, use the hotkey to first select a region to capture from (default hotkey: `CTRL+SHIFT+F3`). The selected region does not need to be very precise, but need to contain the text to translate.

* Finally, use the hotkey to translate what is shown in the region (default: `CTRL+F3`). This will display a window with the original text and the translated text. **Make sure to close this window before requesting another translation, else it won't work** (because of the GUI waiting loop).

* Tip: if the software has difficulties in recognizing the characters (you get gibberish and non-letters characters instead of words), first try to redefine the region with CTRL+F2 and make sure the region includes all text with some margin but not too much of the background (the tighter around the text, the less the OCR will be confused by the background, this can help a lot!). You can use the region selection and translation hotkey to do both in a streamlined fashion (default: `CTRL+F2`).

* Tip2: Try to make the game screen bigger. The bigger the characters, the easier for the OCR to work.

**IMPORTANT NOTE:** The software is still in alpha stage (and may forever stay in this state). It IS working, but sometimes the hotkeys glitch and they do not work anymore. If this happens, simply focus the Python console and hit `CTRL+C` to force quit the app, then launch it again. The selected region is saved in the config file, so you don't have to redo this step everytime.

## Shortcomings & advantages

Compared to UGT, the translated text is not overlaid over a screenshot of the original text. This could maybe be done as Tesseract provides some functions (`image_to_boxes()` or `image_to_osd()` or `image_to_data()`). PRs are very welcome if anyone would like to give it a try!

UGT can also directly select and translate the active window. We dropped this feature because it's platform dependent, so a region selection seemed like the most reliable and cross-platform way to implement screen capture, even if it adds one additional step.

On the other hand, there are several advantages to our approach:

* it's cross-platform (Windows & Linux currently, MacOSX could be supported if we find a python module to register global hotkeys on it),

* we use Tesseract so that OCR is done locally (instead of via the Google Cloud Vision API) so we only send text which is a lot smaller footprint and thus less expensive (generally free), and a big advantage is that it's possible to freely resize the game window to a bigger size, with bigger characters improving the OCR recognition, and also no downscaling/quality reduction is necessary since there is no image transfer,

* Regions can be selected, so that unnecessary screen objects that may confuse the OCR can be elimited with a carefully selected region,

* We enforce the source and target languages, so that both the OCR and translator know what to expect, instead of trying to autodetect, which may fail particularly when there are names that may be written in another language or character form (eg, not in Kanji).

## License

This software is made by Stephen Larroque and is published under the MIT Public License.
