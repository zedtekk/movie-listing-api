import logging
import logging.handlers


PAPERTRAIL_HOST = 'logs6.papertrailapp.com'
PAPERTRAIL_PORT = 11123

handler = logging.handlers.SysLogHandler(address=(PAPERTRAIL_HOST, PAPERTRAIL_PORT))

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[handler]
)

def get_logger(name):
    logger = logging.getLogger(name)
    return logger