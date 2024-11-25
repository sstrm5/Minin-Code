from dataclasses import dataclass


@dataclass
class ServiceException(Exception):
    @property
    def message(self):
        return 'Application exception occured'
