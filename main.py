from __future__ import print_function
import os
import logging
import threading
import time
import contextlib
import shutil


@contextlib.contextmanager
def output(filepath):
    tmp = filepath + '.tmp'
    with open(tmp, 'w') as f:
        yield f
    try:
        try:
            os.replace(tmp, filepath)
        except AttributeError:
            os.rename(tmp, filepath)
    except OSError:
        try:
            os.remove(filepath)
            os.rename(tmp, filepath)
        except OSError:
            shutil.copy2(tmp, filepath)
            os.remove(tmp)


def read_open_kernel(path):
    logging.info("opening %s...", path)
    with open(path) as _:
        time.sleep(1.)
    logging.info("closed %s", path)


def test01():
    path = 'hello.txt'
    with open(path, 'wt') as fp:
        print('hello', file=fp)
    logging.info("created %s", path)

    read_open = threading.Thread(target=read_open_kernel, args=(path,))
    read_open.start()
    try:
        time.sleep(0.5)
        logging.info("trying to apply output() to %s", path)
        with output(path) as fp:
            print('goodbye', file=fp)
        logging.info("successfully returned from open()")
        with open(path) as fp:
            dat = fp.read(999)
            logging.info("now it contains %r", dat)
    except OSError as ex:
        logging.warning("got %r", ex, exc_info=True)
    finally:
        read_open.join(1.)
    logging.info('bye')


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        datefmt='%H:%M:%S',
        format='%(asctime)s.%(msecs)03d %(levelname)s %(filename)s:%(lineno)d:%(funcName)s %(message)s')

    test01()
    logging.info('bye')


if __name__ == '__main__':
    main()
