import simple_comms as comms
from simple_settings import settings
for i in range(10):
    m=comms.recieve(settings.BROADCAST_IP, settings.PORT)
    if m[1][0]
    print(m[0])

