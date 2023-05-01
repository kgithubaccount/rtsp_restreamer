# RTSP Restreamer

This project is a Python-based RTSP (Real-Time Streaming Protocol) restreamer that uses GStreamer and GstRtspServer libraries. It is designed to restream multiple input RTSP streams to new endpoints, as specified in a configuration file.


This project utilizes Docker to simplify the installation process and manage dependencies. Make sure you have Docker installed on your system. If not, please follow the official Docker installation guide.

Once Docker is installed, navigate to the project directory and build the Docker image by running:

```sh
docker build -t rtsp-restreamer .
```
This command builds a Docker image containing the necessary dependencies and the application code, using the provided Dockerfile.

## Usage

To run the RTSP restreamer, execute the following command:

```sh
docker run -p 8554:8554 rtsp-restreamer
```
This command runs the Docker container, exposing port 8554 for the RTSP server.

The restreamed RTSP streams can be accessed at `rtsp://localhost:8554/endpoint`, where endpoint is the path specified in the `config.txt` file.

## Configuration

The `config.txt` file contains the input RTSP stream URLs and their corresponding endpoint paths. Each line in this file has two fields separated by a space. The first field is the input RTSP stream URL, and the second field is the endpoint path for the restreamed output.

### Example of config.txt:

```bash
rtsp://example.stream1.com/stream1 /stream1
rtsp://example.stream2.com/stream2 /stream2
rtsp://example.stream3.com/stream3 /stream3
```
To add or modify restream configurations, edit the config.txt file and rebuild the Docker image.