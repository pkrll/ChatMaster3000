from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint
from core.cmserverfactory import CMServerFactory

if __name__ == "__main__":
    endpoint = TCP4ServerEndpoint(reactor, 9000)
    endpoint.listen(CMServerFactory())
    reactor.run()
