### Proposal for a communications protocol for the ChatMaster 3000
This document will establish the communications protocol used by the **ChatMaster 3000**.

*The ChatMaster 3000 is a retro style chat application, mimicking the look of, we imagine, chat programs in the 1980s.*

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
```
The last two types are only used by the server.

###### Message
A message is a package sent from one user to others connected to the server. The ``data`` attribute consist of an array containing the message, like so:
```json
{
  "type": "message",
  "data": {
    "message": "Hello World!"
  }
}
```
###### Command
A command is a package sent from the user, meant to be read and interpreted by the server. The ``data`` attribute consist of an array, containing the command and a parameter, that can either be a value or a JSON array.
```json
{
  "type": "command",
  "data": {
    "command": "login",
    "parameter": {
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
A notification is a package sent from the server to all clients, as a means to notify everyone on the server and/or in a specific room of an event. The ``data`` attribute of a request consist of an array describing the event.
```json
{
  "type": "notification",
  "data": {
    "event_type": "new_user",
    "message": "User Foo has join the room Bar"
  }
}
```
A list of possible notifications are shown [below](#data-types).
#### Data Types
###### Commands
* login
* rename
* join
* leave

###### Requests
* login

###### Notifications
* user_joined
* user_left
* user_rename
