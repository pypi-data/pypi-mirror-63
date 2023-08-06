import os
import shutil
import click

@click.command()
@click.option("-f", "--from-encoding", help="source encoding.")
@click.option("-t", "--to-encoding", help="destination encoding.")
@click.argument("src", nargs=1, required=True)
@click.argument("dst", nargs=1, required=True)
def copy(from_encoding, to_encoding, src, dst):
    src = src.encode("utf-8")
    dst = dst.encode(to_encoding)
    for root, folders, files in os.walk(src):
        for file in files:
            src_file = os.path.join(root, file)
            rel_src_file = os.path.relpath(src_file, start=src)
            dst_file = os.path.join(dst, rel_src_file.decode(from_encoding).encode(to_encoding))
            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            shutil.copyfile(src_file, dst_file)
            print("copy to {0}".format(dst_file.decode(to_encoding)))


if __name__ == "__main__":
    copy()
