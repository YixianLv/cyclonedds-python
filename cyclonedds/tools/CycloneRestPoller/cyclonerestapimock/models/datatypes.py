from typing import Optional, List
from pydantic import BaseModel
import uuid


Qos = dict


class SystemInfo(BaseModel):
    goop: int
    blub: int
    mega: float


class DcpsParticipant(BaseModel):
    guid: uuid.UUID
    qos: Qos


class DcpsEndpoint(BaseModel):
    guid: uuid.UUID
    participant_guid: uuid.UUID
    participant_instance_handle: int
    topic_name: str
    topic_guid: uuid.UUID
    type_name: str
    qos: Qos


class RemoteParticipant(DcpsParticipant):
    locators: List[str]


class LocalParticipant(DcpsParticipant):
    hyper: int
    downer: float


class RemoteReader(DcpsEndpoint):
    locators: List[str]
    matched_local_writers: List[uuid.UUID]


class LocalReader(DcpsEndpoint):
    matched_local_writers: List[uuid.UUID]
    matched_remote_writers: List[uuid.UUID]


class RemoteWriter(DcpsEndpoint):
    locators: List[str]
    matched_local_readers: List[uuid.UUID]


class LocalWriter(DcpsEndpoint):
    matched_local_readers: List[uuid.UUID]
    matched_remote_readers: List[uuid.UUID]
    retransmit_count: int
    throttled_count: int
    history_cache_size: int


class Topic(BaseModel):
    guid: uuid.UUID
    topic_name: str
    type_name: str
    qos: Qos
    participant_guid: uuid.UUID
    local_writers: List[uuid.UUID]
    local_readers: List[uuid.UUID]
    remote_writers: List[uuid.UUID]
    remote_readers: List[uuid.UUID]

class GuidCollection(BaseModel):
    guids: List[uuid.UUID]
