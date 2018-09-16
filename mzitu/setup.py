import logging

from mzitu.main import main

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    logging.info('--- start ---')
    main()
