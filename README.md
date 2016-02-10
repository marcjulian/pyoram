PyORAM
====================
Crypto tool written in python which stores files on a cloud storage and disguises the access of the files

## Features

### Architecture

![overview](/docs/Architecture.png?raw=true "overview")

### Keys

![key.map](/docs/crypto/keymap.png?raw=true "key.map")

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
