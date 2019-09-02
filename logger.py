import logging
import os

import psycopg2


class DBHandler(logging.Handler):
    def __init__(self, user, password, database, host, port):
        super(DBHandler, self).__init__()
        self.conn = psycopg2.connect(
            user=user,
            password=password,
            database=database,
            host=host,
            port=port
        )

    def emit(self, record):
        msg = record.__dict__
        details = ""
        if msg.get('exc_info'):
            traceback = msg['exc_info']
            details = str(traceback[1])
        with self.conn.cursor() as conn:
            conn.execute('''INSERT INTO logs (log_level, message, details) values (%s, %s, %s)''',
                         (msg['levelname'].upper(), msg['msg'], details))
        self.conn.commit()


def init_db_logger():
    logger = logging.getLogger('db_logger')

    db_handler = DBHandler(
        os.getenv('POSTGRES_USER', 'postgres'),
        os.getenv('POSTGRES_PASSWORD', 'postgres'),
        os.getenv('POSTGRES_DB', 'postgres'),
        os.getenv('POSTGRES_HOST', 'postgres'),
        os.getenv('POSTGRES_PORT', 5432))

    # db_handler.setLevel(logging.NOTSET)
    logger.addHandler(db_handler)
    logger.setLevel(logging.INFO)
    return logger


db_logger = init_db_logger()
