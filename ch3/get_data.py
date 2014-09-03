from __future__ import print_function, division, with_statement

import sys
from functools import partial
from urllib2 import urlopen
from contextlib import closing
from cStringIO import StringIO
import tarfile
from gzip import GzipFile
from tempfile import SpooledTemporaryFile
from itertools import chain

def main(
    data_url,
    open_url=urlopen,
    open_tarfile=tarfile.open,
    buffer_=SpooledTemporaryFile,
    output="data",
):
    with closing(open_url(data_url)) as url_file:
        print("Downloading Data")
        with buffer_(
            max_size=128*1024**2,
            mode='w+b',
        ) as buff:
            def read(f, chunk_size=1024 ** 2):
                print('.', end='')
                sys.stdout.flush()

                data_chunk = f.read(chunk_size)

                return data_chunk

            data_chunks = iter(partial(read, url_file), '')
            map(
                buff.write,
                data_chunks
            )
            print()
            buff.seek(0)
            print("Opening Data")
            #from ipdb import set_trace; set_trace()

            with open_tarfile(
                fileobj=buff,
                mode='r|gz'
            ) as compressed_data_file:
                print("unpacking Data")
                compressed_data_file.extractall(path=output)

if __name__ == "__main__":
    main(
        data_url="http://qwone.com/%7Ejason/20Newsgroups/20news-bydate.tar.gz"
        #data_url="file:///home/jim/Downloads/20news-bydate.tar.gz"
    )
