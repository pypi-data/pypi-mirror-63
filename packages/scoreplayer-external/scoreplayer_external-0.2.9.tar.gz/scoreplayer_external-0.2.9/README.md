# scoreplayer-external

A python module for drawing to the canvas mode of the Decibel ScorePlayer. This allows for OSC messages to be sent to canvas objects in a python-like manner. It requires the python-osc and zeroconf modules.

This is an early version and the documentation is currently incomplete. Until then, a paper explaining its use will be available in the proceedings of the 2018 Australian Computer Music Conference.

# Basic Usage
First you need to create a scorePlayerExternal object and run the selectServer method.
```python
from scoreplayer_external import scoreObject, scorePlayerExternal
import time
from threading import Event

finished = Event()
external = scorePlayerExternal()
external.selectServer()
canvas = external.connect(onConnect)
finished.wait()
external.shutdown()
```
This will check the network for any running iPad servers and prompt the user to connect to one. The drawing commands themselves should be placed into the connection handler method that is passed to the external.connect method.

Some sample drawing commands. Stay tuned for more documentation.
```python
def onConnect():
    canvas.clear()
    scroll = canvas.addScroller('scroll', 1, 10, 10, 300, 300, 500, 20.0)
    scroll.loadImage('modulation.png')
    line = canvas.addLayer('line', 1, 20, 10, 5, 300)
    line.setColour(0, 0, 0)
    clef = scroll.addGlyph('clef', 1, 100, 100)
    clef.setGlyphSize(72)
    clef.setGlyph('fClef')
    bunny = canvas.addLayer('bunny', 0, 200, 200, 300, 300)
    bunny.loadImage('distortion.png', 1)
    line2 = canvas.addLine('line2', 0, 400, 400, 500, 500, 2)
    scroll.start()
    scroll.fade(0, 5)
    bunny.move(100, 400, 8)
    time.sleep(5)
    scroll.fade(1, 5)
    time.sleep(2)
    scroll.stop()
    scroll.setScrollerPosition(0)
    line2.setStartPoint(400, 500)
    line2.setColour(255, 0, 0)
    finished.set()
```
