from enum import Enum

class Status(Enum):
    SAVED = "saved"
    APPLIED = "applied"
    INTERVIEWED = "interviewed"
    OFFERED = "offered"
    REJECTED = "rejected"
    ACCEPTED = "accepted"
    WITHDRAWN = "withdrawn"