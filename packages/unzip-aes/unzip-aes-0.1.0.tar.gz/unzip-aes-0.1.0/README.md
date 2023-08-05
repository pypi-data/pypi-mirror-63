# unzip-aes

Unzip AES encrypted zip file.

## Install

```shell
pip install unzip-aes
```

## Installed Utils

- unzip-aes


## Usage

```shell
C:\Code\unzip-aes256>python unzip-aes.py --help
Usage: unzip-aes.py [OPTIONS] ZIPFILE [DST]

  Unzip AES encrypted zip file.

Options:
  -p, --password TEXT  [required]
  --help               Show this message and exit.
```

## Example

**Example1:**

Unzip the-target.zip file to current folder.

```shell
unzip-aes -p Password the-target.zip
```

**Example2:**

Unzip the-target.zip file to dst folder

```shell
unzip-aes -p Password the-target.zip dst
```

## Release

### v0.1.0 2020/03/11

- First release.