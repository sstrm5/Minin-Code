from dataclasses import dataclass
import datetime


@dataclass
class CustomerEntity:
    id: str
    email: str
    first_name: str
    last_name: str
    created_at: datetime
