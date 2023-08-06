# Nameko Sematext Logger

## Get Started

```
pip install nameko-sematext-logger
```

## config.yaml

```
SEMATEXT:
    KEY: ${SEMATEXT_KEY:<DEFAULT_KEY_HERE>}
    URL: <URL_HSER>
    PORT: 514
```

## service_file.py
```
from nameko_sematext import logger

class GreetingService:
    sematext_logger = logger.Sematext()

    ...
    def create_card(self, request):
        ...
        self.sematext_logger.critical('This is a critical log')
        self.sematext_logger.info('This is an info log')
        self.sematext_logger.warning('This is a warning log')
        self.sematext_logger.error('This is an error log')
        ...
```