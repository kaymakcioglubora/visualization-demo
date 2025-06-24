from dataclasses import dataclass
from datetime import datetime


@dataclass
class NetworkMeasurement:
    """
    Network Measurement Entity data class
    Time: datettime

    """
    #TODO: Apply entity diagrams
    time: datetime
    value: str
