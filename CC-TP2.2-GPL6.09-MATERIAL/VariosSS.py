import threading
from ss import SS


SSlist = [SS("./dummyConfigSS.txt", portNumber, 1000, "") for portNumber in range(1025,1030)]

for ss in SSlist:
    t = threading.Thread(target = ss.run)
    t.start()
