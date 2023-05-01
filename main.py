import sys
import gi
import time
import logging

import os
os.environ['GST_DEBUG'] = '*:3' 

gi.require_version("Gst", "1.0")
gi.require_version("GstRtspServer", "1.0")
from gi.repository import Gst, GstRtspServer, GLib

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

Gst.init(None)


class StreamRestreamer:
    def __init__(self, server, input_url, endpoint):
        self.server = server
        self.input_url = input_url
        self.endpoint = endpoint

    def on_rtspsrc_error(self, bus, message):
        (error, debug) = message.parse_error()
        logger.error(f"Error received for {self.input_url}: {error.message}. Retrying in 5 seconds.")
        GLib.timeout_add(5000, self.reconnect_src, bus)

    def reconnect_src(self, src):
        logger.info(f"Reconnecting to {self.input_url}...")
        src.set_property("location", self.input_url)
        return False

    def create_pipeline_str(self):
        pipeline_str = (
            f"rtspsrc location={self.input_url} protocols=tcp name=src ! "
            f"rtph264depay ! rtph264pay name=pay0 pt=96"
        )
        logger.debug(f"Pipeline string for {self.input_url}: {pipeline_str}")

        pipeline = Gst.parse_launch(pipeline_str)

        src = pipeline.get_by_name("src")
        src.connect("pad-added", self.on_rtspsrc_pad_added)
        src.connect("pad-removed", self.on_rtspsrc_pad_removed)
        src.connect("new-manager", self.on_new_manager)

        bus = pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message::error", self.on_rtspsrc_error)

        return pipeline_str

    def on_rtspsrc_pad_added(self, src, pad):
        logger.info(f"New pad added to {self.input_url}: {pad.get_name()}")

    def on_rtspsrc_pad_removed(self, src, pad):
        logger.info(f"Pad removed from {self.input_url}: {pad.get_name()}")

    def on_new_manager(self, src, manager):
        logger.info(f"Connected to {self.input_url}")

    def on_client_connected(self, server, client):
        connection = client.get_connection()
        if connection:
            remote_address = connection.get_ip()
            if remote_address:
                logger.info(f"Client connected: {remote_address}")
            else:
                logger.warning("Unable to get client's remote address")
        else:
            logger.warning("Unable to get client's connection")

    def restream(self):
        factory = GstRtspServer.RTSPMediaFactory()
        factory.set_launch(self.create_pipeline_str())
        factory.set_shared(True)
        self.server.get_mount_points().add_factory(self.endpoint, factory)

        self.server.connect("client-connected", self.on_client_connected)


def main(args):
    config_file = 'config.txt'

    with open(config_file, "r") as f:
        stream_configs = [line.strip().split() for line in f.readlines()]

    # Initialize GStreamer with debug logging
    Gst.init(["--gst-debug-level=4"])

    server = GstRtspServer.RTSPServer.new()
    server.set_address("0.0.0.0")
    server.set_service("8554")
    

    for input_url, endpoint in stream_configs:
        restreamer = StreamRestreamer(server, input_url, endpoint)
        restreamer.restream()
        logger.info(f"Restreaming {input_url} at rtsp://localhost:8554{endpoint}")

    server.attach(None)

    logger.info("RTSP server running...")

    GLib.MainLoop().run()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
