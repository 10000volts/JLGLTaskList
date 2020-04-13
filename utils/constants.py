from utils.enums import enum

TASK_STATUS = enum(WAITING=0, ACCEPTED=1)
TASK_STATUS_CHOICES = [
    (TASK_STATUS.WAITING, '待接收'),
    (TASK_STATUS.ACCEPTED, '已接收'),
]