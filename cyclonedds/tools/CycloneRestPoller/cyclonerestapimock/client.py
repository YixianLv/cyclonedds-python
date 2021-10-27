#!/usr/bin/env python3
from http.client import HTTPConnection
import uuid
import json
import sys
import datetime
import argparse
import urwid

from models.datatypes import SystemInfo, Topic, RemoteParticipant, LocalParticipant, RemoteReader, LocalReader, RemoteWriter, LocalWriter, GuidCollection
from ui import palette, NodeWidget

guid = str(uuid.uuid4())


def create_parser(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--runtime", type=float, help="Limit the runtime of the tool, in seconds.")
    args = parser.parse_args(args)
    return args


class CycloneAPI():
    def __init__(self, url):
        self.conn = HTTPConnection(url)

    def connect(self, path):
        self.conn.request("GET", path)

        response = self.conn.getresponse()
        if response.status != 200:
            raise Exception(f"{response.status}: {response.reason}")

        return json.loads(response.read().decode())

    def system_info(self):
        data = self.connect("/system")
        return SystemInfo(
            goop=data["goop"],
            blub=data["blub"],
            mega=data["mega"]
            )

    def topics(self):
        data = self.connect("/topic")
        return GuidCollection(guids=data["guids"])

    def local_participants(self):
        data = self.connect("/local/participant")
        return GuidCollection(guids=data["guids"])

    def remote_participants(self):
        data = self.connect("/remote/participant")
        return GuidCollection(guids=data["guids"])

    def local_participant(self):
        data = self.connect(f"/local/participant/{guid}")
        return LocalParticipant(
            guid=data["guid"],
            qos=data["qos"],
            hyper=data["hyper"],
            downer=data["downer"]
            )

    def remote_participant(self):
        data = self.connect(f"/remote/participant/{guid}")
        return RemoteParticipant(
            guid=data["guid"],
            qos=data["qos"],
            locators=data["locators"]
            )

    def local_participant_readers(self):
        data = self.connect(f"/local/participant/{guid}/readers")
        return GuidCollection(guids=data["guids"])

    def local_participant_writers(self):
        data = self.connect(f"/local/participant/{guid}/writers")
        return GuidCollection(guids=data["guids"])

    def remote_participant_readers(self):
        data = self.connect(f"/remote/participant/{guid}/readers")
        return GuidCollection(guids=data["guids"])

    def remote_participant_writers(self):
        data = self.connect(f"/remote/participant/{guid}/writers")
        return GuidCollection(guids=data["guids"])

    def local_readers(self):
        data = self.connect("/local/reader")
        return GuidCollection(guids=data["guids"])

    def remote_readers(self):
        data = self.connect("/remote/reader")
        return GuidCollection(guids=data["guids"])

    def local_writers(self):
        data = self.connect("/local/writer")
        return GuidCollection(guids=data["guids"])

    def remote_writers(self):
        data = self.connect("/remote/writer")
        return GuidCollection(guids=data["guids"])

    def local_reader(self):
        data = self.connect(f"/local/reader/{guid}")
        return LocalReader(
            guid=data["guid"],
            participant_guid=data["participant_guid"],
            participant_instance_handle=data["participant_instance_handle"],
            topic_name=data["topic_name"],
            topic_guid=data["topic_guid"],
            type_name=data["type_name"],
            qos=data["qos"],
            matched_local_writers=data["matched_local_writers"],
            matched_remote_writers=data["matched_remote_writers"]
            )

    def remote_reader(self):
        data = self.connect(f"/remote/reader/{guid}")
        return RemoteReader(
            guid=data["guid"],
            participant_guid=data["participant_guid"],
            participant_instance_handle=data["participant_instance_handle"],
            topic_name=data["topic_name"],
            topic_guid=data["topic_guid"],
            type_name=data["type_name"],
            qos=data["qos"],
            locators=data["locators"],
            matched_local_writers=data["matched_local_writers"]
            )

    def local_writer(self):
        data = self.connect(f"/local/writer/{guid}")
        return LocalWriter(
            guid=data["guid"],
            participant_guid=data["participant_guid"],
            participant_instance_handle=data["participant_instance_handle"],
            topic_name=data["topic_name"],
            topic_guid=data["topic_guid"],
            type_name=data["type_name"],
            qos=data["qos"],
            matched_local_readers=data["matched_local_readers"],
            matched_remote_readers=data["matched_remote_readers"],
            retransmit_count=data["retransmit_count"],
            throttled_count=data["throttled_count"],
            history_cache_size=data["history_cache_size"]
        )

    def remote_writer(self):
        data = self.connect(f"/remote/writer/{guid}")
        return RemoteWriter(
            guid=data["guid"],
            participant_guid=data["participant_guid"],
            participant_instance_handle=data["participant_instance_handle"],
            topic_name=data["topic_name"],
            topic_guid=data["topic_guid"],
            type_name=data["type_name"],
            qos=data["qos"],
            locators=data["locators"],
            matched_local_readers=data["matched_local_readers"]
            )

    def call_local(self):
        return (
            self.system_info(),
            self.topics(),
            self.local_participants(),
            self.local_participant(),
            self.local_participant_readers(),
            self.local_participant_writers(),
            self.local_readers(),
            self.local_writers(),
            self.local_reader(),
            self.local_writer(),
            )

    def call_remote(self):
        return (
            self.system_info(),
            self.topics(),
            self.remote_participants(),
            self.remote_participant(),
            self.remote_participant_readers(),
            self.remote_participant_writers(),
            self.remote_readers(),
            self.remote_writers(),
            self.remote_reader(),
            self.remote_writer(),
            )

    def output_all(self):
        for method in self.call_all():
            print(f"{method.__class__.__name__}: {method}\n")


def main(sys_args):
    args = create_parser(sys_args)
    api = CycloneAPI("localhost:8000")
    node1 = NodeWidget("Node 1's opinion of Node 1").create_widget(api)
    node2 = NodeWidget("Node 2's opinion of Node 1").create_widget(api)
    columns = urwid.Columns([node1, node2])

    try:
        time_start = datetime.datetime.now()
        v = True
        while v:
            loop = urwid.MainLoop(columns, palette)
            loop.run()
            if args.runtime:
                v = datetime.datetime.now() < time_start + datetime.timedelta(seconds=args.runtime)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
