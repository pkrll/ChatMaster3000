
def createJSONPackage(data):
    """
        Returns a JSON package.

        Args:
            data (dict) :   A dictionary consisting of the data to JSONify.
    """
    import json
    return json.dumps(data)

def newPackage(packageType, data):
    """
    """
    return createJSONPackage({
        "type": packageType,
        "data": data
    })

def newMessage(message):
    """
    """
    return newPackage("message", {"message": message})

def newCommand(command, parameters=None):
    """
    """
    return newPackage("command", {"command": command, "parameters": parameters})

def localTime():
    """
    """
    import time
    from collections import namedtuple

    timeStruct = time.localtime()
    # A value below 10 will not include the leading 0.
    hour = str(timeStruct.tm_hour) if timeStruct.tm_hour >= 10 else "0" + str(timeStruct.tm_hour)
    minutes = str(timeStruct.tm_min) if timeStruct.tm_min >= 10 else "0" + str(timeStruct.tm_min)
    seconds = str(timeStruct.tm_sec) if timeStruct.tm_sec >= 10 else "0" + str(timeStruct.tm_sec)
    LocalTime = namedtuple("localTime", "hour minutes seconds")

    return LocalTime(hour=hour, minutes=minutes, seconds=seconds)
