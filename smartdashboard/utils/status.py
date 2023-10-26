from enum import Enum


class StatusEnum(Enum):
    RUNNING = "Running"
    COMPLETED = "Completed"
    FAILED = "Failed"
    PENDING = "Pending"
    INACTIVE = "Inactive"
    UNSTABLE = "Unstable"


GREEN_RUNNING = f":green[{StatusEnum.RUNNING.value}]"
GREEN_COMPLETED = f":green[{StatusEnum.COMPLETED.value}]"
RED_UNSTABLE = f":red[{StatusEnum.UNSTABLE.value}]"
RED_FAILED = f":red[{StatusEnum.FAILED.value}]"
