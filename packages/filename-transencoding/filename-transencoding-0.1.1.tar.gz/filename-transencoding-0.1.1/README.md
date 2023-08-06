# filename-transencoding

Fix filename encoding problem. Copy all files to new position with new encoding.

## Install

```shell
pip install filename-transencoding
```

## Installed Utils

- filename-transencoding

## Usage

```shell
[root@www tmp]# filename-transencoding --help
Usage: filename-transencoding [OPTIONS] SRC DST

Options:
  -f, --from-encoding TEXT  source encoding.
  -t, --to-encoding TEXT    destination encoding.
  --help                    Show this message and exit.
[root@www tmp]# filename-transencoding -f gbk -t utf-8 src-folder dst-folder

```

## Releases

### v0.1.1 2020/03/18

- Remove click version, so will NOT requires lastest click version.

### v0.1.0 2020/03/18

- First release.