import logging

logging.basicConfig(filename="sample.log",
                    filemode='w',
                    format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')