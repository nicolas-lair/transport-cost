from .cost import MyTransporter
from .constant import TransporterParams
from .app_custom import MyDashCustomComponent


class Geodis(MyTransporter, TransporterParams, MyDashCustomComponent):
    pass