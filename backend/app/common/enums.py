from enum import StrEnum


class JobStatus(StrEnum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    DONE = "DONE"
    FAILED = "FAILED"
    
class MediaType(StrEnum):
    VOICE = "voice"
    PHOTO = "photo"