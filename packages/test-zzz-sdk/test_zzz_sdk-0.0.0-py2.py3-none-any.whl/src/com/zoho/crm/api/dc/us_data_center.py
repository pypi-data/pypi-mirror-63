try:
    from source.dc.data_center import DataCenter
except Exception as e:
    from .data_center import DataCenter


class USDataCenter(DataCenter):
    def get_iamurl(self):
        return "https://accounts.zoho.com/oauth/v2/token"

    @classmethod
    def PRODUCTION(cls):
        return DataCenter.Environment("https://www.zohoapis.com",cls().get_iamurl())

    @classmethod
    def SANDBOX(cls):
        return DataCenter.Environment("https://sandbox.zohoapis.com/crm/v2", cls().get_iamurl())

    @classmethod
    def DEVELOPER(cls):
        return DataCenter.Environment("https://developer.zohoapis.com/crm/v2", cls().get_iamurl())


