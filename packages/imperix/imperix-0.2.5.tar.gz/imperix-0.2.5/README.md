# Imperix Node SDK - Python

## Overview

**Imperix** is a new fleet control *philosophy*, not just a *ground control program*. **Imperix** connects an entire fleet to the internet using secured and encrypted communication protocols, and provides a command center interface to all units on the fleet.

The **Imperix Node SDK** is a set of open-source *Software Developer Kits* in common programming languages allowing users to connect and interface custom *autopilot* systems with the **Imperix Cloud**.

The core functionality of the **SDK** includes:
* Authenticating node with the **Imperix Cloud**
* Synchronizing mission state with the cloud
* Streaming manual control commands from the cloud
* Streaming telemetry, video, and data to the cloud


## Installation

All dependencies for the **Imperix Node SDK** Python implementation are provided in the *requirements.txt* file. To install the dependencies, run the following command:

```sh
pip3 install -r requirements.txt
```


## Setup

The SDK requires a *node configuration* file ***node.cfg*** to be placed in the program's root directory. The *node configuration* requires the following parameters:
* Unique node identifier string provided upon node registration
* Node authorization access key provided upon node registration
* Imperix Commander API URL (standard)
* Streamer/Stream Controller IP address/URL available in fleet manager

The ***node.cfg*** file may be downloaded from the Imperix Commander node configuration page.


## Usage

The **Imperix Node SDK** is designed to authenticate the node and initialize communications in its own thread. Review detailed SDK documentation available on: https://docs.imperix.ai.

To use the SDK functions, import the SDK into your Python workspace/project using:

```python
import asyncio
from imperix import NodeLink
```

### Async/Await Operations

The NodeLink handlers and communication threads use the **asyncio** package's ***async/await*** calls for concurrent operations. In order to set this up correctly, an event loop must be created and handled.

See the example below for a main file definition:

```python
# Developed by Aptus Engineering, Inc. <https://aptus.aero>
# See LICENSE.md file in project root directory

import asyncio
from imperix import NodeLink


# Set up callback functions
# Called when mission is updated
async def missionUpdateCallback(mission):
    print(mission)


# Called with manual control command is received
async def manualControlCallback(control):
    print(control)


# Instantiate node link with callbacks
node = NodeLink(
    missionUpdateCallback=missionUpdateCallback,
    manualControlCallback=manualControlCallback
)


async def main():
    
    # Connect and authenticate
    await node.connect()

    # Main loop...
    while True:
        await asyncio.sleep(1)
        print("hello")


# Start event loop
eventLoop = asyncio.get_event_loop()

try:
    asyncio.ensure_future(main())               # Main thread
    eventLoop.run_forever()

except KeyboardInterrupt:
    pass

finally:
    eventLoop.close()

asyncio.get_event_loop().run_until_complete(NodeLinkThread(node))
asyncio.get_event_loop().run_forever()
```


### Initialization and Recieve Commands

Initialize a communication stream with the **Imperix Cloud** using the following command:

```python
node = NodeLink(
    missionUpdateCallback=handleMissionUpdate,
    manualControlCallback=handleManualControl
)
```

Where:
* **handleMissionUpdate** is a callback/lambda function which accepts the updated mission as a dictionary.
* **handleManualControl** is a callback/lambda function which accepts manual control command as a dictionary.

To connect to the ***Imperix Cloud***, use the following command:

```
await node.connect(config='node.cfg')
```

Where **config** is the path to the *node configuration* file.


### Sending Mission Updates

In order to update mission parameters, call the function:
```python
await node.updateMission(
    activeWaypoint=wptIdx,
    missionStatus=status
)
```

Where:
* **wptIdx** is a dict key to the waypoint index the node is currently moving to/on.
* **status** is a string defining the current mission status. It can be one of:
    * **Standby** if the mission is loaded but not active
    * **Active** if the node is performing the loaded mission.
    * **Complete** if the node successfully finished the mission
    * **Failed:[ERROR]** if the node failed the mission. **[ERROR]** must be replaced with the reason for mission failure 


### Streaming Data

Three kinds of data streams are available to send to the **Imperix Cloud**. Users can send one of:
* **Telemetry** - live data representing critical node status, such as location, velocities, attitude, etc.
* **Video/Image** - live or pre-captured video/image feeds for live view on the **Imperix Commander** or for future analytics using **Imperix Intelligence**.
* **Data** - any JSON-serializable data strings, such as sensor readings, messages etc.

In order to stream telemetry, construct a dictionary with keys indicating the following variables:

* ATT_ROLL (degrees)
* ATT_PITCH (degrees)
* ATT_HEADING (degrees)
* LOC_LATITUDE (degrees)
* LOC_LONGITUDE (degrees)
* LOC_ALTITUDE (meters)
* VEL_GROUNDSPEED (meters per second)
* VEL_AIRSPEED (meters per second)
* VEL_VERTICAL_SPEED (meters per second)
* VEL_ROLL_RATE (degrees per second)
* VEL_PITCH_RATE (degrees per second)
* VEL_YAW_RATE (degrees per second)
* STS_BATTERY (percentage 0-100)
* STS_SIGNAL (percentage 0-100)

And call the function:

```python
await node.transmitTelemetry(telemetry)
```

Where **telemetry** is the dict with the above variables.

In order to stream image, either provide the image as a 1 or 3 channel numpy array to the function:

```python
await node.transmitImage(
    image,
    timeStamp=timestamp,
    feed=feed
)
```

Where:
* **image** is the numpy image,
* **timestamp** is a *datetime* object, or *None* to use current timestamp (live feed), and
* **feed** is a string identifying the name of the video feed. Default is *PRIMARY*.

A pre-compressed JPEG image binary (avaiable using OpenCV, or Pillow) can also be streamed by calling the function:

```python
await node.transmitImageBinary(
    image,
    timeStamp=timestamp,
    feed=feed
)
```

Where **image** is the pre-compressed JPEG image binary as a **bytes** object.


To stream an encoded MPEG(-4) video from a live camera, streaming can be started using the call:

```python
await node.streamVideoFromSource(feed, source)
```

Where **source** is a string representing the camera source ***(eg. /dev/video0)***.

Videos can also be streamed from files by replacing the **source** argument with the file name, and by passing the **isFile** flag to the call:

```python
await node.streamVideoFromSource(feed, source, isFile=True)
```


Finally, to stream data to the **Imperix Cloud**, the following function may be called:

```python
await node.transmitData(data)
```

Where **data** is a dictionary with JSON-serializable keys-value pairs.


### Streaming Latency Feedback

A mechanism is built to allow in optimizing video/image frame-rate and latency. Every second, an image/video feedback packet is sent back to the node, whose data can be used to adjust the stream quality accordingly. The following variables can be used to access framerate and latency.

```python
node.imageFrameRate
node.imageLatency
```


### Ending Session

In order to close out of a session - to be used when disconnecting the node, performing updates, or shutting down the node, the following function may be called:

```python
await node.disconnect()
```

Shutting down the node, or exiting the program also automatically disconnects the node from the **Imperix Cloud**.