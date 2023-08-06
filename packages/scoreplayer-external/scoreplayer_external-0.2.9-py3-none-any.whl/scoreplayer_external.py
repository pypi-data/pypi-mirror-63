#!/usr/bin/env python3
"""

Python external for controlling the Decibel ScorePlayer canvas mode, v0.2.9
Copyright (c) 2018 Aaron Wyatt

This module provides a python wrapper for sending OSC canvas commands to the
Decibel ScorePlayer.


This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

from zeroconf import ServiceBrowser, Zeroconf, ServiceStateChange
from pythonosc import osc_message_builder, udp_client, dispatcher, osc_server
import time
import socket
import threading
from datetime import datetime
from itertools import zip_longest
from queue import Queue

#Convenience function from itertools recipes
def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

#The scoreObject class is used to provide a python representation of objects
#drawn onto the ScorePlayer canvas. It is subclassed for specific object types.
class scoreObject:
    _addressPrefix = '/Renderer/Command/'
    
    def __init__(self, name, external):
        self.name = name
        self.external = external
        self.removed = False

    #Every object can have its colour set.
    def setColour(self, r, g, b, a=255):
        self.sendCommand('setColour', int(r), int(g), int(b), int(a))

    #The method used to actually send the OSC command via our external object.
    #It checks to make sure that the object hasn't already been removed on the player.
    def sendCommand(self, command, *args):
        if self.removed:
            print ('{} has been removed'.format(self.name))
            return
        self.external.sendMessage(scoreObject._addressPrefix + self.name + '/' + command, *args)

class scoreNonLineObject(scoreObject):
    #Commands common to all objects but lines.
    #(Abstract class not used for actual objects)
    def addLayer(self, objname, part, x, y, width, height):
        self.sendCommand('addLayer', objname, part, int(x), int(y), int(width), int(height))
        return scoreLayerObject(objname, self.external)

    def addScroller(self, objname, part, x, y, width, height, scrollerWidth, speed):
        self.sendCommand('addScroller', objname, part, int(x), int(y), int(width), int(height), int(scrollerWidth), float(speed))
        return scoreScrollerObject(objname, self.external)

    def addText(self, objname, part, x, y, fontSize=36):
        self.sendCommand('addText', objname, part, int(x), int(y), float(fontSize))
        return scoreTextObject(objname, self.external)

    def addGlyph(self, objname, part, x, y, glyphSize=36):
        self.sendCommand('addGlyph', objname, part, int(x), int(y), float(glyphSize))
        return scoreGlyphObject(objname, self.external)

    def addStave(self, objname, part, x, y, width, height, lineWidth):
        self.sendCommand('addStave', objname, part, int(x), int(y), int(width), int(height), int(lineWidth))
        return scoreStaveObject(objname, self.external)

    def addLine(self, objname, part, x1, y1, x2, y2, lineWidth):
        self.sendCommand('addLine', objname, part, int(x1), int(y1), int(x2), int(y2), int(lineWidth))
        return scoreLineObject(objname, self.external)

class scoreNonLineCanvasObject(scoreNonLineObject):
    #Commands common to all objects but lines and the canvas.
    def remove(self):
        self.sendCommand('remove')
        self.removed = True

    def setOpacity(self, opacity):
        self.sendCommand('setOpacity', float(opacity))

    def fade(self, opacity, duration):
        self.sendCommand('fade', float(opacity), float(duration))

    def setPosition(self, x, y):
        self.sendCommand('setPosition', int(x), int(y))

    def move(self, x, y, duration):
        self.sendCommand('move', int(x), int(y), float(duration))
    
class scoreCanvasObject(scoreNonLineObject):
    def clear(self):
        self.sendCommand('clear')

class scoreLineObject(scoreObject):
    def remove(self):
        self.sendCommand('remove')
        self.removed = True

    def setOpacity(self, opacity):
        self.sendCommand('setOpacity', float(opacity))

    def fade(self, opacity, duration):
        self.sendCommand('fade', float(opacity), float(duration))

    def setWidth(self, width):
        self.sendCommand('setWidth', int(width))

    def setStartPoint(self, x, y):
        self.sendCommand('setStartPoint', int(x), int(y))

    def setEndPoint(self, x, y):
        self.sendCommand('setEndPoint', int(x), int(y))

class scoreLayerObject(scoreNonLineCanvasObject):
    def loadImage(self, imgname, autosizing=0):
        self.sendCommand('loadImage', imgname, autosizing)

    def clearImage(self):
        self.sendCommand('clearImage')

    def setSize(self, width, height):
        self.sendCommand('setSize', int(width), int(height))

class scoreScrollerObject(scoreLayerObject):
    #This inherits from the Layer Object. This may need to change in future.
    def setScrollerWidth(self, scrollerWidth):
        self.sendCommand('setScrollerWidth', int(scrollerWidth))

    def setScrollerPosition(self, scrollerPosition):
        self.sendCommand('setScrollerPosition', int(scrollerPosition))

    def setScrollerSpeed(self, scrollerSpeed):
        self.sendCommand('setScrollerSpeed', float(scrollerSpeed))

    def start(self):
        self.sendCommand('start')

    def stop(self):
        self.sendCommand('stop')

class scoreTextObject(scoreNonLineCanvasObject):
    def setText(self, text):
        self.sendCommand('setText', text)

    def setFont(self, font):
        self.sendCommand('setFont', font)

    def setFontSize(self, fontSize):
        self.sendCommand('setFontSize', float(fontSize))

class scoreGlyphObject(scoreNonLineCanvasObject):
    def setGlyph(self, glyphType):
        self.sendCommand('setGlyph', glyphType)

    def setGlyphSize(self, glyphSize):
        self.sendCommand('setGlyphSize', float(glyphSize))

class scoreStaveObject(scoreNonLineCanvasObject):
    def clear(self):
        self.sendCommand('clear')
    
    def setSize(self, width, height):
        self.sendCommand('setSize', int(width), int(height))
    
    def setLineWidth(self, lineWidth):
        self.sendCommand('setLineWidth', int(lineWidth))

    def setClef(self, clef, position):
        self.sendCommand('setClef', clef, int(position))

    def removeClef(self, position):
        self.sendCommand('removeClef', int(position))

    def addNotehead(self, note,  position, filled=1):
        self.sendCommand('addNotehead', note, int(position), int(filled))

    def addNote(self, note, position, duration):
        self.sendCommand('addNote', note, int(position), int(duration))

    def removeNote(self, note, position):
        self.sendCommand('removeNote', note, int(position))

class scorePlayerExternal:
    #The protocol version expected. Current version is 16.
    protocolVersion = 16
    
    def __init__(self):
        self.__services = {}
        self.listeningPort = 7000
        self.__service = None
        self.__connectionHandler = None
        self.errorHandler = None
        self.__statusHandler = None
        self.__clientListHandler = None
        self.playHandler = None
        self.pauseHandler = None
        self.resetHandler = None
        self.tickHandler = None
        self.loadHandler = None
        self.seekHandler = None
        self.seekingHandler = None
        self.extMessageHandler = None
        self.printTicks = False
        self.printMessages = False
        self.printTimestamp = True
        self.printToQueue = False
        self.printQueue = Queue()
        self.__location = 0

        self.__zeroconf = None
        self.__connected = False
        self.__registrationTimer = None
        
        #Set up our message routing and start listening on our port.
        self.__dispatcher = dispatcher.Dispatcher()
        self.__dispatcher.map('/Server/*', self.__printMessage)
        self.__dispatcher.map('/Control/*', self.__printMessage)
        self.__dispatcher.map('/External/*', self.__extMessage)
        
        self.__dispatcher.map('/Server/RegistrationOK', self.__onConnect)
        self.__dispatcher.map('/Server/BadProtocolVersion', self.__onError)
        self.__dispatcher.map('/External/NewServer', self.__onReconnect)
        self.__dispatcher.map('/Control/Play', self.__onPlay)
        self.__dispatcher.map('/Control/Pause', self.__onPause)
        self.__dispatcher.map('/Control/Reset', self.__onReset)
        self.__dispatcher.map('/Control/Seek', self.__whileSeeking)
        self.__dispatcher.map('/Control/SeekFinished', self.__onSeek)
        self.__dispatcher.map('/Tick', self.__onTick)
        self.__dispatcher.map('/Server/LoadComplete', self.__onLoad)
        self.__dispatcher.map('/Server/RequestRejected', self.__onError)
        self.__dispatcher.map('/External/Error', self.__onError)
        self.__dispatcher.map('/Status', self.__statusReceived)
        self.__dispatcher.map('/Server/ClientList', self.__clientListReceived)

        #Start our zeroconf browser.
        self.__startBonjour()

        #If our port is unavailable, increase the port number by 1 and try again.
        while True:
            try:
                self.__server = osc_server.ThreadingOSCUDPServer(('0.0.0.0', self.listeningPort), self.__dispatcher)
                break
            except:
                self.listeningPort += 1
            
        self.__server_thread = threading.Thread(target=self.__server.serve_forever)
        self.__server_thread.start()
        print('Listening on port {}'.format(self.listeningPort))

    def __startBonjour(self):
        if self.__zeroconf == None:
            #Set up our service browser
            self.__services.clear()
            self.__zeroconf = Zeroconf()
            self.__browser = ServiceBrowser(self.__zeroconf, '_decibel._udp.local.', handlers=[self.__serviceChange])
            time.sleep(1)

    def __stopBonjour(self):
        if self.__zeroconf != None:
            self.__browser.cancel()
            self.__zeroconf.close()
            self.__zeroconf = None

    def __parseServiceName(self, service):
        serverName = service.server
        scoreName = service.name
        if serverName.endswith('.local.'):
            serverName = serverName[:-7]
        scoreName = scoreName[:(scoreName.find(service.type)) - 1]
        scoreName = scoreName[:(scoreName.rfind('.'))]
        return [serverName, scoreName]

    def findServers(self):
        self.__startBonjour()
        serverList = []
        for service in self.__services.values():
            serverDetails = self.__parseServiceName(service)
            address = socket.inet_ntoa(service.address)
            serverList.append([*serverDetails, address, service.port])
        return serverList

    def selectServer(self):
        self.__startBonjour()
    
        while True:
            i = 1
            print('Choose an iPad to connect to')
            servers = []
            #List each service we've discovered
            for service in self.__services.values():
                serverDetails = self.__parseServiceName(service)
                print('{}: {} ({})'.format(i, serverDetails[0], serverDetails[1]))
                #Save the service info to an array
                servers.append(service)
                i += 1
            print('Or\n{}: Refresh List'.format(i))
            while True:
                try:
                    selection = int(input('Enter Selection: '))
                except ValueError:
                    print('Invalid selection')
                    continue

                if selection == i:
                    print()
                    break
                elif selection >= i or selection < 0:
                    print('Invalid selection')
                else:
                    self.__service = servers[selection - 1]
                    return

    def connect(self, connectionHandler, errorHandler=None):
        if self.__service is None:
            print('No server selected')
            return
        
        #Connect to our server
        address = socket.inet_ntoa(self.__service.address)
        return self.connectToAddress(address, self.__service.port, connectionHandler, errorHandler)

    def __registrationTimeout(self):
        self.__printMessage('/External/RegistrationTimeout', 'Connection timed out')
        self.__onError('/External/RegistrationTimeout', 'Connection timed out')
        self.__registrationTimer = None

    #Connect to a specified address and port. This can be used if the required service cannot
    #be found using zeroconf.
    def connectToAddress(self, address, port, connectionHandler=None, errorHandler=None):
        if self.__connected:
            #Disconnect if we're connected.
            self.disconnect()
            
        #Stop our zeroconf browser
        self.__stopBonjour()

        self.__connectionHandler = connectionHandler
        self.errorHandler = errorHandler
        
        self.__client = udp_client.SimpleUDPClient(address, port)
        self.__client.send_message('/Server/RegisterExternal', ['Decibel Networking Protocol v' + str(scorePlayerExternal.protocolVersion), self.listeningPort])        
        if self.__registrationTimer != None:
            self.__registrationTimer.cancel()
        self.__registrationTimer = threading.Timer(5, self.__registrationTimeout)
        self.__registrationTimer.start()

        if self.__connectionHandler is not None:
            return scoreCanvasObject('canvas', self)
    
    def sendMessage(self, message, *args):
        if not self.__connected:
            print('Not connected')
            return
        self.__client.send_message(message, args)

    def __serviceChange(self, zeroconf, service_type, name, state_change):
        if state_change is ServiceStateChange.Added:
            self.__services[name] = zeroconf.get_service_info(service_type, name)
        elif state_change is ServiceStateChange.Removed:
            del self.__services[name]

    def __onConnect(self, oscAddress):
        if self.__registrationTimer != None:
            self.__registrationTimer.cancel()
            self.__registrationTimer = None
        self.__connected = True
        if self.__connectionHandler is not None:
            handler = self.__connectionHandler
            self.__connectionHandler = None
            #time.sleep(0.1)
            handler()

    def __onError(self, oscAddress, *oscArgs):
        if self.errorHandler is not None:
            if len(oscArgs) > 0:
                self.errorHandler(oscAddress, oscArgs[0])
            else:
                self.errorHandler(oscAddress, None)

    def __onPlay(self, oscAddress):
        if self.playHandler is not None:
            self.playHandler()

    def __onPause(self, oscAddress, location):
        self.__location = location
        if self.pauseHandler is not None:
            self.pauseHandler(location)

    def __onReset(self, oscAddress):
        self.__location = 0
        if self.resetHandler is not None:
            self.resetHandler()

    def __whileSeeking(self, oscAddress, location):
        self.__location = location
        if self.seekingHandler is not None:
            self.seekingHandler(location)

    def __onSeek(self, oscAddress):
        if self.seekHandler is not None:
            self.seekHandler(self.__location)

    def __onTick(self, oscAddress, location):
        self.__printMessage(oscAddress, location)
        self.__location = location
        if self.tickHandler is not None:
            self.tickHandler(location)

    def __extMessage(self, oscAddress, *oscArgs):
        self.__printMessage(oscAddress, *oscArgs)
        #Add capabilites here later
        if oscAddress == "/External/NewServer" or oscAddress == "/External/Error":
            #These are dealt with elsewhere.
            return
        if self.extMessageHandler is not None:
            self.extMessageHandler(oscAddress, *oscArgs)

    def __onLoad(self, oscAddress):
        self.__location = 0
        if self.loadHandler is not None:
            self.loadHandler()

    def __statusReceived(self, oscAddress, *oscArgs):
        self.__printMessage(oscAddress, *oscArgs)
        if self.__statusHandler is not None:
            if len(oscArgs) < 7:
                #We don't have the right number of arguments.
                return
            #Format our status message into a dictionary.
            status = {
                "name": oscArgs[0],
                "composer": oscArgs[1],
                "scoreType": oscArgs[2],
                "scoreVersion": oscArgs[3],
                "playerState": oscArgs[4],
                "location": oscArgs[5],
                "duration": oscArgs[6]
                }
            handler = self.__statusHandler
            self.__statusHandler = None
            handler(status)

    def __clientListReceived(self, oscAddress, *oscArgs):
        if self.__clientListHandler is not None:
            clientList = []
            for device,version in grouper(oscArgs, 2):
                currentClient = {
                    "deviceName": device,
                    "version": version
                    }
                clientList.append(currentClient)
            handler = self.__clientListHandler
            self.__clientListHandler = None
            handler(clientList)
    
    def __printMessage(self, oscAddress, *oscArgs):
        if oscAddress == '/Tick':
            if not self.printTicks:
                return
        elif not self.printMessages:
            return
        argsString = ''
        for arg in oscArgs:
            if isinstance(arg, str):
                argsString += '"{}", '.format(arg)
            else:
                argsString += '{}, '.format(arg)
        if len(argsString) > 1:
            argsString = argsString[:-2]
        if self.printTimestamp:
            outString = '{}: {} {}'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), oscAddress, argsString)
        else:
            outString = '{} {}'.format(oscAddress, argsString)
        if self.printToQueue:
            outString = outString.rstrip()
            self.printQueue.put(outString)
        else:
            #Explicitly print our newline so it isn't separated from the message when multiple
            #messages arrive at the same time.
            outString = outString.rstrip() + '\n'
            print(outString, end="")

    #Connect our external to a new device if the old server has left the network.
    def __onReconnect(self, oscAddress, address, port):
        self.connectToAddress(address, port)

    def disconnect(self):
        self.sendMessage('/Server/UnregisterExternal', self.listeningPort)
        self.__connected = False

    def shutdown(self):
        self.disconnect()
        self.__server.shutdown()
        #Stop bonjour on the off chance that it is running
        self.__stopBonjour()

    #Commands to easily send basic control signals to the iPad
    def play(self):
        self.sendMessage('/Control/Play')

    def pause(self, location=-1):
        if location == -1:
            location = self.__location
        self.sendMessage('/Control/Pause', float(location))

    def reset(self):
        self.sendMessage('/Control/Reset')

    def loadScore(self, name, composer, scoreType, scoreVersion='0'):
        self.sendMessage('/Server/LoadRequest', name, composer, scoreType, scoreVersion)

    def getStatus(self, statusHandler):
        self.__statusHandler = statusHandler
        self.sendMessage('/Master/GetStatus')

    def getClientList(self, clientListHandler):
        self.__clientListHandler = clientListHandler
        self.sendMessage('/Server/GetClientList')
