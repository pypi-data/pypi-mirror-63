try:
    from source.dc.data_center import DataCenter
except Exception as e:
    from .data_center import DataCenter


class AUDataCenter(DataCenter):
    def get_iamurl(self):
        return "https://accounts.zoho.com.au/oauth/v2/token"

    @classmethod
    def PRODUCTION(cls):
        return  DataCenter.Environment("https://www.zohoapis.com.au/crm/v2", cls().get_iamurl())

    @classmethod
    def SANDBOX(cls):
        return DataCenter.Environment("https://sandbox.zohoapis.com.au/crm/v2",cls(). get_iamurl())

    @classmethod
    def DEVELOPER(cls):
        return DataCenter.Environment("https://developer.zohoapis.com.au/crm/v2",cls(). get_iamurl())
