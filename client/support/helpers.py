
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
