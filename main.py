import os
import logging
import threading
import time


def read_open_kernel(path):
    logging.info("opening %s...", path)
    with open(path) as fp:
        time.sleep(1.)
    logging.info("closed %s", path)


def test01():
    path = 'hello.txt'
    with open(path, 'wt') as fp:
        fp.write('hello\n')
    logging.info("created %s", path)

    read_open = threading.Thread(target=read_open_kernel, args=(path,))
    read_open.start()
    try:
        time.sleep(0.1)
        logging.info("trying to remove %s", path)
        os.remove(path)
        logging.info("successfully removed %s", path)
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
