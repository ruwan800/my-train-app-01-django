import logging, traceback
logger = logging.getLogger(__name__)

class ExceptionMiddleware(object):

    def process_exception(self, request, exception):
        logger.debug(traceback.format_exc())
        return