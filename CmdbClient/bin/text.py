# from Sansa import models
# from django.core.exceptions import ObjectDoesNotExist


class hehe(object):

    def __init__(self):
        self.mandatory_fields = ['sn', 'asset_id', 'asset_type']
        self.response = {'error': [], 'info': [], 'warning': []}

    def response_msg(self, msg_type, key, msg):
        if msg_type in self.response:
            self.response[msg_type].append({key: msg})
        else:
            raise ValueError

    def mandatory_check(self, data, only_check_sn=False):
        for field in self.mandatory_fields:
            if field not in data:
                self.response_msg('error', 'MandatoryCheckFailed',
                                  "The field [%s] is mandatory and not provided in your reporting data" % field)
        else:  # 如果检测字段没问题，也就没有返回
            if self.response['error']:
                print("走到字段检测返回false")
                return False
        try:
            if not only_check_sn:  # 默认走这个
                # self.asset_obj = models.Asset.objects.get(id=int(data['asset_id']), sn=data['sn'])
                print(data['asset_id'], data['sn'])
            else:
                # self.asset_obj = models.Asset.objects.get(sn=data['sn'])
                print(data['sn'])
            return True
        except:
            self.response_msg('error', 'AssetDataInvalid',
                              "Cannot find asset object in DB by using asset id [%s] and SN [%s] " % (
                                  data['asset_id'], data['sn']))
            self.waiting_approval = True
            print("找不到数据库数据返回false")
            return False


data = {'asset_id': None, 'model': 'hehe1', 'sn': '123', 'asset_type': 'server'}

a = hehe()
print(a.mandatory_check(data,only_check_sn=True))