PyORAM
====================
Crypto tool written in python which stores files on a cloud storage and disguises the access of the files using Path ORAM (Oblivious RAM protocol).

## Table of contents

* [Quick start](#quick-start)
* [Features](#features)
* [Screenshots](#screenshots)
* [Under construction](#under-construction)
* [Acknowledgements](#acknowledgements)
* [Copyright and license](#copyright-and-license)

## Quick start

1. Clone the repo: `git clone https://github.com/marcjulian/pyoram.git`.
2. Install Python 3.4 (developed and tested with Python 3.4.4).
3. Install dependencies for Python (using [pip](https://pip.pypa.io/en/stable/installing/) or visit the website for instructions).
  * [crypthography 1.3.1](https://cryptography.io/en/latest/) `pip install cryptography==1.3.1`.
  * [kivy 1.9.1](https://kivy.org/#download)
  * [dropbox 6.1](https://www.dropbox.com/developers/documentation/python#install) `pip install dropbox==6.1`.
4. Register a [Dropbox API app and generate a access token](https://www.dropbox.com/developers/documentation/python#tutorial) using Dropbox [App Console](https://www.dropbox.com/developers/apps) (an active Dropbox account is necessary).
5. Run `src/pyoram/main.py` and enter your password.
6. For the first time an error will occur, replace "My token" in the cloud map with your token `"token": "My token"`, the map can be found in `data/cloud.map`.
7. Restart the program and re-enter password -> now it should start to initialize the cloud (check your folder).
8. Configurations to the program can be made in `src/pyoram/core/config.py` including:
  * Block size
  * Height of the Path ORAM tree
9. Resetting the program:
  * Delete the `data/stash` folder, `data/position.map`, `data/file.map` and set `"init": true` to false in `data/cloud.map` (you can keep the `data/key.map`)
  * Delete the `data/key.map`, if you like to select a new password (perform the previous step to avoid decryption errors)

## Features

### Architecture

<img src="/docs/Architecture.png?raw=true" width="500">

### Keys

<img src="/docs/crypto/keymap.png?raw=true" width="700">

### Confidentiality

- file encryption with AES(256-bit key length)
- CBC-mode with IV(128-bit)
- padding the data with PKCS7

### Authentication

- HMAC(256-bit key length) using SHA256

## Screenshots


## Under construction

PyORAM is currently under construction and further features will be added shortly.
For more information visit the kanban board at [Taiga.io](https://tree.taiga.io/project/marcjulian-pyoram/).

## Acknowledgements

The project is the main task of my internship at SIIT in the study program Business Information Systems (Bachelor of Science).
Prof. Dr. Steve Gordon is the advisor, who helps defining the requirements for the project and assists me with any further questions.

The final presentation of my internship is available on [prezi](https://prezi.com/4i5lkurr0bgh/pyoram/).

## Copyright and license

Code and documentation copyright 2016 marcjulian. Code released under [the MIT license](https://github.com/marcjulian/pyoram/blob/master/LICENSE.md). Docs released under [Creative Commons](https://github.com/marcjulian/pyoram/blob/master/docs/LICENSE).
