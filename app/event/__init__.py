import logging

from django.conf import settings


class ServiceNameFormatter(logging.Formatter):
    def __init__(self, service_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service_name = service_name
        self.env_name = settings.ENV_NAME

    def format(self, record):
        record.msg = f"[{self.env_name}][{self.service_name}] {record.msg}"
        return super().format(record)


logger = logging.getLogger(settings.BX_LOGGER)
handler = logging.StreamHandler()
handler.setFormatter(ServiceNameFormatter("BX"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)
