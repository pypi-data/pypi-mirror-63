from nameko.extensions import DependencyProvider

import logging

class Sematext(DependencyProvider):

    def setup(self):
        self.sematext_config = self.container.config.get('SEMATEXT')
        self.tracking_key = self.sematext_config.get('KEY', None)
        self.tracking_url = self.sematext_config.get('URL', None)
        self.tracking_port = self.sematext_config.get('PORT', None)

    def get_dependency(self, worker_ctx):
        
        def custom_logger():
            handler = logging.handlers.SysLogHandler(address=(self.tracking_url, self.tracking_port))
            formater = logging.Formatter("{}:%(message)s".format(self.tracking_key))
            handler.setFormatter(formater)
            logger = logging.getLogger("sematext")
            logger.setLevel(logging.DEBUG)
            logger.addHandler(handler)
            return logger

        return custom_logger()