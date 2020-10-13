from ronglian_sms_sdk import SmsSDK

accId = '8aaf070874af41ee0175021bb5671b81'
accToken = '1f221c5988a84f0caecd08caae5d44e8'
appId = '8aaf070874af41ee0175021bb6451b88'


def send_message():
    sdk = SmsSDK(accId, accToken, appId)
    tid = '1'
    mobile = '15904925186'
    datas = ('变量1', '变量2')
    resp = sdk.sendMessage(tid, mobile, datas)
    print(resp)
class CCP(object):
    """发送短信的单例类"""
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,'_instance'):
            cls._instance = super(CCP,cls).__new__(cls,*args,**kwargs)
            cls._instance.sdk = SmsSDK(accId, accToken, appId)
        return cls._instance
    def send_message(self,tid,mobile,datas):
        result = self._instance.sdk.sendMessage(tid,mobile,datas)
        result = result.split(':')
        print(result)
        if result[1] == "000000":
            return 1
        else:
            return 0



if __name__ == '__main__':
    CCP().send_message('1','15904925186',('123456','5'))