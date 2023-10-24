from enum import Enum


class StatusEnum(Enum):
    RUNNING = "Running"
    COMPLETED = "Completed"
    FAILED = "Failed"
    PENDING = "Pending"
    INACTIVE = "Inactive"
    UNSTABLE = "Unstable"


class StatusColors(Enum):
    GREEN_RUNNING = f":green[{StatusEnum.RUNNING}]"
    GREEN_COMPLETED = f":green[{StatusEnum.COMPLETED}]"
    RED_INACTIVE = f":red[{StatusEnum.INACTIVE}]"
    RED_UNSTABLE = f":red[{StatusEnum.UNSTABLE}]"
    RED_FAILED = f":red[{StatusEnum.FAILED}]"
