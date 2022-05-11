import logging

logging.basicConfig(filename="app.log",
                    filemode='w',
                    format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')