from pytz import timezone
from datetime import datetime

timestamp = str(datetime.now(timezone("Asia/Seoul")).strftime("%y-%m-%d %H:%M:%S"))
print(timestamp) 