try:
    from source.dc.data_center import DataCenter
except Exception as e:
    from .data_center import DataCenter


class INDataCenter(DataCenter):
    def get_iamurl(self):
        return "https://accounts.zoho.in/oauth/v2/token"

    @classmethod
    def PRODUCTION(cls):
        return DataCenter.Environment("https://www.zohoapis.in/crm/v2", cls().get_iamurl())

    @classmethod
    def SANDBOX(cls):
        return  DataCenter.Environment("https://sandbox.zohoapis.in/crm/v2", cls().get_iamurl())

    @classmethod
    def DEVELOPER(cls):
        return DataCenter.Environment("https://developer.zohoapis.in/crm/v2",cls().get_iamurl())

