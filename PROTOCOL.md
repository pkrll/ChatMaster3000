# Proposal for a communications protocol for the ChatMaster 3000

*__NOTE:__ This document may be subject to changes.*

## Overview

### The Client
The ChatMaster 3000 client is a fully text-based application, that runs in the terminal. The client has a simple user interface with a chat log and a message box.

Besides messages, the client can also send commands to the server. [See below for more information.](#command)

### The Server
The ChatMaster 3000 server is a terminal-based application that listens on the TCP port 9000 for incoming connections. The server can accept multiple connections simultaneously, allowing for users to chat with each other.

The server keeps track of the user and assigns them each with a unique identifier, used internally. New clients all join a general "chat room", but can create and join different rooms. The server is responsible for rerouting messages to the correct room.

A message sent to the server should only be rerouted to the users in that room, except the sending user.

### Packages
The communication between the ChatMaster 3000 server and client consist of small JSON objects sent over TCP. All packages sent back and forth are in JSON format and have the same basic structure, including the attributes ``type`` and ``data``. The JSON data should preferably also be compressed before sent and decompressed when received.

#### Package Types
Listed below are the different values the ``type`` attribute can have:
```json
{ "type": "message", "data": {} }
{ "type": "command", "data": {} }
{ "type": "request", "data": {} }
{ "type": "notification", "data": {} }
{ "type": "session", "data": {} }
{ "type": "error", "data": {} }

```
The last four types are only used by the server.

###### Message
A message is a package sent from one user to others connected to the server. The ``data`` attribute consist of an array containing the message, like so:
```json
{
  "type": "message",
  "data": {
    "message": "Hello World!",
    "username": "SomeUser"
  }
}
```
###### Command
A command is a package sent from the user, meant to be read and interpreted by the server. The ``data`` attribute consist of an array, containing the command and a JSON array.
```json
{
  "type": "command",
  "data": {
    "command": "login",
    "parameters": {
      "username": "PythonMaster2K16"
    }
  }
}
```
A list of possible commands can be found [below](#data-types).
###### Request
A request is a package sent from the server to a client. The client sends back an appropriate response in the form of a command. The ``data`` attribute of a request consist simply of a attribute/value-pair describing the request.
```json
{
  "type": "request",
  "data": {
    "request": "login"
  }
}
```
A list of possible requests are shown [below](#data-types).
###### Notification
A notification is a package sent from the server to all clients, as a means to notify everyone on the server and/or in a specific room of an event. The ``data`` attribute of a notification consist of an array describing the event.
```json
{
  "type": "notification",
  "data": {
    "event_type": "user_joined",
    "username": "someUser"
  }
}
```
A list of possible notifications are shown [below](#data-types).
###### Session
A session is a package sent from the server to a client, when the connection has been established and the client is trying to join the server. The ``data`` attribute will contain a boolean, indicating whether the client successfully joined the server, a ``reason`` string on failure or a ``channels`` array on success.
```json
{
  "type": "session",
  "data": {
    "status": 1,
    "channels": ["Channel 1", "Channel 2"]
  }
}
```
###### Error
An error is a package sent from the server to a client, when an error with a command occurs. The ``data`` attribute of an error consist of an array describing the error event, with the ``error_type`` attribute matching the command.
```json
{
  "type": "error",
  "data": {
    "error_type": "private",
    "message": "Channel cannot be set to private."
  }
}
```
See the [commands](#data-types) list below for a list of possible errors.
#### Package and Data Types
##### Commands
* [login](#login)
* [rename](#rename)
* [join](#join)
* [leave](#leave)
* [private](#private)
* [public](#public)
* [channels](#channels)

###### login
Sent as a response to a login request. Data parameter should include the username:
```json
  {"username": "someUserName"}
```

###### rename
Request to change username to the specified username. Data parameter should include the username:

```json
  {"username": "someUserName"}
```

###### join
Join or create a new channel. Data parameter should include the channel name:
```json
  {"channel": "someChannel"}
```

###### leave
Leave the current channel.

###### private

Set current channel to private.

###### public

Set current channel to public.

###### channels

Get a list of public channels.

##### Requests
* login

##### Notifications
**channel_list**:

Consists of a JSON object with data attributes: ```channels```.

**user_joined**:

Consists of a JSON object with data attributes: ```username```.

**user_left**:

Consists of a JSON object with data attributes: ```username```.

**user_rename**:

Consists of a JSON object with data attributes: ```old_username``` and ```new_username```.

## The connection process
When a client establishes connection with the server, the server will send a ``login`` request asking for the username. The client must respond with a command of same type ``login`` and in the ``parameter`` array supply the username, as shown below.

###### Server request:
```json
{
  "type": "request",
  "data": {
    "request": "login"
  }
}
```

###### Response:
```json
{
  "type": "command",
  "data": {
    "command": "login",
    "parameters": {
      "username": "PythonMaster2K16"
    }
  }
}
```
The server will send back a ``session`` message. The ``data`` attribute indicates if the user is allowed to join the server. If the username is already taken, the attribute ``status`` will have value of ``False``, effectively denying connection. Otherwise the server will send a ``True`` value.
```json
{
  "type": "session",
  "data": {
    "status": 0,
    "reason": "Username is already taken."
  }
}

{
  "type": "session",
  "data": {
    "status": 1,
    "channels": ["Channel1", "ChuckNorris", "Google"]
  }
}


```
