try:
    from source.dc.data_center import DataCenter
except Exception as e:
    from .data_center import DataCenter


class EUDataCenter(DataCenter):
    def get_iamurl(self):
        return "https://accounts.zoho.eu/oauth/v2/token"

    @classmethod
    def PRODUCTION(cls):
        return DataCenter.Environment("https://www.zohoapis.eu/crm/v2",cls().get_iamurl())

    @classmethod
    def SANDBOX(cls):
        return DataCenter.Environment("https://sandbox.zohoapis.eu/crm/v2", cls().get_iamurl())

    @classmethod
    def DEVELOPER(cls):
        return DataCenter.Environment("https://developer.zohoapis.eu/crm/v2", cls().get_iamurl())

