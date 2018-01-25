import logging
import logging.handlers
import os

# get file path
pwd = os.path.abspath(os.path.dirname(__file__))
log_dir = os.path.join(pwd, 'Logs')

if not os.path.exists(log_dir):
    os.mkdir(log_dir)

class Log(object):
    filename = os.path.join(log_dir, 'ipool.log')
    handler = logging.handlers.RotatingFileHandler(filename, mode='a', maxBytes=1024 * 1024, backupCount=10,
                                                   encoding=None, delay=False)

    formatter = logging.Formatter('%(asctime)s - %(filename)s - %(threadName)s - %(levelname)s  %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(logging.NOTSET)

    @classmethod
    def getLogger(self, name='root', level=logging.DEBUG):
        log = logging.getLogger(name)
        log.setLevel(level)
        log.addHandler(self.handler)
        return log


if __name__ == '__main__':
    # useage
    x = Log.getLogger('You')
    x.info('X%sfefef', 'eeeeeee')
