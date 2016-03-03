PyORAM
====================
Crypto tool written in python which stores files on a cloud storage and disguises the access of the files

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

- HMAC(265-bit key length) using SHA256

## Dependencies
- crypthography
- kivy
- dropbox

## Under construction

PyORAM is currently under construction and further features will be added shortly.
For more information visit the kanban board at [Taiga.io](https://tree.taiga.io/project/marcjulian-pyoram/).

## Acknowledgements

The project is the main task of my internship at SIIT in the study program Business Information Systems (Bachelor of Science).
Prof. Dr. Steve Gordon is the advisor, who helps defining the requirements for the project and assists me with any further questions.

## Copyright and license

Code and documentation copyright 2016 marcjulian. Code released under [the MIT license](https://github.com/marcjulian/pyoram/blob/master/LICENSE.md).
