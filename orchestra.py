#!/usr/bin/env python3

import subprocess, time
from haloserverquery.haloserverquery import queryServer



class HaloServer:
    """Instance of a halo server running in a tmux session"""

    def __init__(self, name: str, ip: str = "127.0.0.1", port: int = 2302):
        """Initialize"""
        self.__serverName = name
        self.__serverAddress = ip
        self.__serverPort = port
        self.__online = False

    def start(self) -> None:
        """Start the server"""
        if self.__online == False:
            subprocess.run([
                'tmux',
                'new-session',
                '-d',
                '-s',
                f'{self.__serverName}',
                f'wineconsole haloceded.exe -port {self.__serverPort} -path profiles'
            ])
            self.__online = True

    def getPlayerCount(self) -> int:
        """Return the server player count"""
        query = queryServer(self.__serverAddress, self.__serverPort)
        if query is None:
            return 0
        return int(query['numplayers'])

    def sendCommand(self, command: str) -> None:
        """Send a command to the server's tmux session"""
        subprocess.run(['tmux', 'send-keys', '-t', f'{self.__serverName}', f'{command}', 'Enter'])

    def shutdown(self) -> None:
        """Shutdown the server"""
        if self.__online == True:
            self.sendCommand("quit")
            self.__online = False


def main():
    """Main Function"""
    # foo = subprocess.Popen('./run', stdin=subprocess.PIPE)
    #b tmox = subprocess.run(['tmux', 'new-session', '-d', '-s', 'my_session', './run'])
    # tmux new-session -d -s my_session './run'
    # tmux send-keys -t my_session 'quit' Enter

    primaryServer = HaloServer("PrimaryServer", port=2312)
    backupServer = HaloServer("BackupServer", port=2313)
    primaryServer.start()
    launchNew = True
    while True:
        playerCount = primaryServer.getPlayerCount()
        print(f"Player count: {playerCount}")
        print(launchNew)
        if playerCount > 14 and launchNew == True:
            print("Launching new backup server")
            backupServer.start()
            launchNew = False
            print(launchNew)
        if playerCount < 8 and backupServer.getPlayerCount() == 0 and launchNew == False:
            print("Shutting down backup server...")
            backupServer.shutdown()
            launchNew = True

        time.sleep(15)

    # print(remote.getPlayerCount())

if __name__ == "__main__":
    main()
