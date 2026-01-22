from enum import StrEnum


class JobStatus(StrEnum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    
class MediaType(StrEnum):
    VOICE = "voice"
    PHOTO = "photo"