try:
    from source.dc.data_center import DataCenter
except Exception as e:
    from .data_center import DataCenter


class CNDataCenter(DataCenter):
    def get_iamurl(self):
        return "https://accounts.zoho.com.cn/oauth/v2/token"
    @classmethod
    def PRODUCTION(cls):
        return DataCenter.Environment("https://www.zohoapis.com.cn/crm/v2", cls().get_iamurl())
    @classmethod
    def SANDBOX(cls):
        return DataCenter.Environment("https://sandbox.zohoapis.com.cn/crm/v2", cls().get_iamurl())
    @classmethod
    def DEVELOPER(cls):
        return DataCenter.Environment("https://developer.zohoapis.com.cn/crm/v2", cls().get_iamurl())