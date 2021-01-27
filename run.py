import threading
import PeakLearnerWsgi

# start httpServer
server = threading.Thread(target=PeakLearnerWsgi.startServer)


def startServer():
    server.start()


def shutdown():
    PeakLearnerWsgi.shutdownServer()
    server.join()


if __name__ == '__main__':
    try:
        startServer()
    except KeyboardInterrupt:
        shutdown()
