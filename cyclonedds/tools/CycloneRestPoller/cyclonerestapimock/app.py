import uuid
import random
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
from cyclonerestapimock.models.datatypes import SystemInfo, Topic, RemoteParticipant, LocalParticipant, RemoteReader, LocalReader, RemoteWriter, LocalWriter, GuidCollection

app = FastAPI()

@app.get("/system", response_model=SystemInfo, tags=["System"])
async def system_info():
    return SystemInfo(goop=1, blub=1, mega=1.0)

@app.get("/topic", response_model=GuidCollection, tags=["System"])
async def topics():
    return GuidCollection(guids=[uuid.uuid4()])

@app.get("/local/participant", response_model=GuidCollection, tags=["Local", "Participant"])
async def local_participants():
    return GuidCollection(guids=[uuid.uuid4()])

@app.get("/remote/participant", response_model=GuidCollection, tags=["Remote", "Participant"])
async def remote_participants():
    return GuidCollection(guids=[uuid.uuid4()])

@app.get("/local/participant/{guid}", response_model=LocalParticipant, tags=["Local", "Participant"])
async def local_participant(guid: uuid.UUID):
    return LocalParticipant(
        guid=guid,
        qos={},
        hyper=4,
        downer=2.0
        )

@app.get("/remote/participant/{guid}", response_model=RemoteParticipant, tags=["Remote", "Participant"])
async def remote_participant(guid: uuid.UUID):
    return RemoteParticipant(
        guid=guid,
        qos={},
        locators=["192.168.1.100"]
        )

@app.get("/local/participant/{guid}/readers", response_model=GuidCollection, tags=["Local", "Participant"])
async def local_participant_readers(guid: uuid.UUID):
    return GuidCollection(guids=[uuid.uuid4()])

@app.get("/local/participant/{guid}/writers", response_model=GuidCollection, tags=["Local", "Participant"])
async def local_participant_writers(guid: uuid.UUID):
    return GuidCollection(guids=[uuid.uuid4()])

@app.get("/remote/participant/{guid}/readers", response_model=GuidCollection, tags=["Remote", "Participant"])
async def remote_participant_readers(guid: uuid.UUID):
    return GuidCollection(guids=[uuid.uuid4()])

@app.get("/remote/participant/{guid}/writers", response_model=GuidCollection, tags=["Remote", "Participant"])
async def remote_participant_writers(guid: uuid.UUID):
    return GuidCollection(guids=[uuid.uuid4()])

@app.get("/local/reader", response_model=GuidCollection, tags=["Local", "Reader"])
async def local_readers():
    return GuidCollection(guids=[uuid.uuid4()])

@app.get("/remote/reader", response_model=GuidCollection, tags=["Remote", "Reader"])
async def remote_readers():
    return GuidCollection(guids=[uuid.uuid4()])

@app.get("/local/writer", response_model=GuidCollection, tags=["Local", "Writer"])
async def local_writers():
    return GuidCollection(guids=[uuid.uuid4()])

@app.get("/remote/writer", response_model=GuidCollection, tags=["Remote", "Writer"])
async def remote_writers():
    return GuidCollection(guids=[uuid.uuid4()])

@app.get("/local/reader/{guid}", response_model=LocalReader, tags=["Local", "Reader"])
async def local_reader(guid: uuid.UUID):
    return LocalReader(
        guid=guid,
        participant_guid=guid,
        participant_instance_handle=0,
        topic_name="empty",
        topic_guid=guid,
        type_name="empty",
        qos={},
        matched_local_writers=[],
        matched_remote_writers=[]
        )

@app.get("/remote/reader/{guid}", response_model=RemoteReader, tags=["Remote", "Reader"])
async def remote_reader(guid: uuid.UUID):
    return RemoteReader(
        guid=guid,
        participant_guid=guid,
        participant_instance_handle=0,
        topic_name="empty",
        topic_guid=guid,
        type_name="empty",
        qos={},
        locators=["12.1.0.1"],
        matched_local_writers=[]
        )

@app.get("/local/writer/{guid}", response_model=LocalWriter, tags=["Local", "Writer"])
async def local_writer(guid: uuid.UUID):
    return LocalWriter(
        guid=guid,
        participant_guid=guid,
        participant_instance_handle=0,
        topic_name="empty",
        topic_guid=guid,
        type_name="empty",
        qos={},
        matched_local_readers=[],
        matched_remote_readers=[],
        retransmit_count=0,
        throttled_count=0,
        history_cache_size=random.randint(0, 200000000)
    )

@app.get("/remote/writer/{guid}", response_model=RemoteWriter, tags=["Remote", "Writer"])
async def remote_writer(guid: uuid.UUID):
    return RemoteWriter(
        guid=guid,
        participant_guid=guid,
        participant_instance_handle=0,
        topic_name="empty",
        topic_guid=guid,
        type_name="empty",
        qos={},
        locators=["12.1.0.1"],
        matched_local_readers=[]
        )
