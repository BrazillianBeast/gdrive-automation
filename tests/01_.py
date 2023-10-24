import os
from notifypy import Notify

notification = Notify()
notification.title = "GDrive Uploader"
notification.message= "Upload completed"

notification.send()