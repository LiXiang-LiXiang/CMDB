from django.db import models
from django.contrib.auth.models import User
# class UserPofile(User):
#     # name = models.CharField("姓名", max_length=32)
#     mobile = models.CharField(u'手机', max_length=32, unique=True, default=None, blank=True, null=True)
#
#     class Meta:
#         verbose_name = '用户'
#         verbose_name_plural = "用户"
#
#     def __str__(self):
#         return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    phone = models.CharField(u'手机', max_length=32, unique=True, default=None, blank=True, null=True)
    # nik_name = models.CharField(u'昵称', max_length=32, default=None, blank=True, null=True)
    token = models.CharField(u'token', max_length=128, default=None, blank=True, null=True)

    class Meta:
        verbose_name = '用户管理'
        verbose_name_plural = "用户管理"

    def __str__(self):
        return 'user {}'.format(self.user.username)


class Asset(models.Model):
    asset_type_choices = (
        ('server', u'服务器'),
        ('networkdevice', u'网络设备'),
        ('software', u'软件资产'),
    )
    asset_type = models.CharField(choices=asset_type_choices, max_length=64, default='server')
    name = models.CharField(max_length=64, unique=True)
    sn = models.CharField(u'资产SN号', max_length=128, unique=True)
    business_unit = models.ForeignKey('BusinessUnit', on_delete=models.CASCADE, verbose_name=u'所属业务线', null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    # 标签可以让你从多维度去看你的机器分布以及使用状况

    admin = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name=u'资产管理员', null=True, blank=True)
    idc = models.ForeignKey('IDC', on_delete=models.CASCADE, verbose_name=u'IDC机房', null=True, blank=True)
    manufactory = models.ForeignKey('Manufactory', on_delete=models.CASCADE, verbose_name=u'制造商', null=True, blank=True)
    management_ip = models.GenericIPAddressField(u'管理IP', blank=True, null=True)
    contract = models.ForeignKey('Contract', on_delete=models.CASCADE, verbose_name=u'合同', null=True, blank=True)
    trade_date = models.DateField(u'购买时间', null=True, blank=True)
    expire_date = models.DateField(u'过保修期', null=True, blank=True)
    price = models.FloatField(u'价格', null=True, blank=True)

    memo = models.TextField(u'备注', null=True, blank=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, auto_now=True)

    class Meta:
        verbose_name = 'Asset资产总表'
        verbose_name_plural = "Asset资产总表"

    def __str__(self):
        return '<id:%s name:%s>' % (self.id, self.name)


class Server(models.Model):
    """服务器设备,如果是资产关联服务器，那网络设备就无法关联到资产"""
    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    created_by_choices = (
        ('auto', 'Auto'),
        ('manual', 'Manual'),
    )
    created_by = models.CharField(choices=created_by_choices, max_length=32, default='auto')
    hosted_on = models.ForeignKey('self', on_delete=models.CASCADE, related_name='hosted_on_server', blank=True, null=True)  # 自关联，虚拟设备用此字段
    # physical_disk_driver = models.ManyToManyField('Disk', verbose_name=u'硬盘',blank=True,null=True)
    # 得从硬盘表里关联到server，因为是多块硬盘关联到一个服务器上
    model = models.CharField(verbose_name=u'型号', max_length=128, null=True, blank=True)
    raid_type = models.CharField(u'raid类型', max_length=512, blank=True, null=True)
    os_type = models.CharField(u'操作系统类型', max_length=64, blank=True, null=True)
    os_distribution = models.CharField(u'发型版本', max_length=64, blank=True, null=True)
    os_release = models.CharField(u'操作系统版本', max_length=64, blank=True, null=True)

    class Meta:
        verbose_name = 'Server服务器'
        verbose_name_plural = "Server服务器"
        # together = ["sn", "asset"]

    def __str__(self):
        return '%s sn:%s' % (self.asset.name, self.asset.sn)


class NetworkDevice(models.Model):
    """网络设备"""

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_assset_type_choices = (
        (0, '路由器'),
        (1, '交换机'),
        (2, '负载均衡'),
        (4, 'VPN设备'),
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_assset_type_choices, verbose_name="服务器类型", default=0)

    vlan_ip = models.GenericIPAddressField(u'VlanIP', blank=True, null=True)
    intranet_ip = models.GenericIPAddressField(u'内网IP', blank=True, null=True)
    # sn = models.CharField(u'SN号',max_length=128,unique=True)
    # manufactory = models.CharField(verbose_name=u'制造商',max_length=128,null=True, blank=True)
    model = models.CharField(u'型号', max_length=128, null=True, blank=True)
    firmware = models.ForeignKey('Software', blank=True, null=True, on_delete=models.CASCADE)
    port_num = models.SmallIntegerField(u'端口个数', null=True, blank=True)
    device_detail = models.TextField(u'设置详细配置', null=True, blank=True)

    class Meta:
        verbose_name = 'Network网络设备'
        verbose_name_plural = "Network网络设备"

    def __str__(self):
        return '%s sn:%s' % (self.asset.name, self.asset.sn)


class Software(models.Model):
    os_types_choice = (('linux', 'Linux'),
                        ('windows', 'Windows'),
                        ('software', 'Softwares'))
    os_distribution_choices = (('windows','Windows'),
                               ('centos','CentOS'),
                               ('ubuntu', 'Ubuntu'))
    type = models.CharField(u'系统类型', choices=os_types_choice, max_length=64,help_text=u'eg. GNU/Linux',default=1)
    distribution = models.CharField(u'发型版本', choices=os_distribution_choices,max_length=32,default='windows')
    version = models.CharField(u'软件/系统版本', max_length=64, help_text=u'eg. CentOS release 6.5 (Final)', unique=True)

    # language_choices = (('cn',u'中文'),
    #                     ('en',u'英文'))
    # language = models.CharField(u'系统语言',choices = language_choices, default='cn',max_length=32)
    # version = models.CharField(u'版本号', max_length=64,help_text=u'2.6.32-431.3.1.el6.x86_64' )

    def __str__(self):
        return self.version

    class Meta:
        verbose_name = 'Software软件/系统'
        verbose_name_plural = "Software软件/系统"

class CPU(models.Model):
    """CPU组件,不关联到server是因为，网络设备也有CPU、内存条"""
    # 内存可以是不同型号，不同大小,CPU型号主频是一样的，一个资产不管有几个CPU，只有一条记录
    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    cpu_model = models.CharField(u'CPU型号', max_length=128, blank=True)
    cpu_count = models.SmallIntegerField(u'物理cpu个数')
    cpu_core_count = models.SmallIntegerField(u'cpu核数')

    memo = models.TextField(u'备注', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'CPU'
        verbose_name_plural = "CPU"

    def __str__(self):
        return self.cpu_model


class RAM(models.Model):
    """内存组件"""

    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    sn = models.CharField(u'SN号', max_length=128, blank=True, null=True)
    model = models.CharField(u'内存型号', max_length=128)
    slot = models.CharField(u'插槽', max_length=64)
    capacity = models.IntegerField(u'内存大小(MB)')

    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '%s: slot%s: capacity%s' % (self.asset_id, self.slot, self.capacity)

    class Meta:
        verbose_name = 'RAM内存条'
        verbose_name_plural = "RAM内存条"
        unique_together = ("asset", "slot")

    auto_create_fields = ['sn', 'slot', 'model', 'capacity']


class Disk(models.Model):
    """硬盘组件"""

    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    sn = models.CharField(u'SN号', max_length=128, blank=True, null=True)
    slot = models.CharField(u'插槽位', max_length=64)
    # manufactory = models.CharField(u'制造商', max_length=64,blank=True,null=True)
    model = models.CharField(u'磁盘型号', max_length=128, blank=True, null=True)
    capacity = models.FloatField(u'磁盘容量GB')
    disk_iface_choice = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSD', 'SSD'),
    )

    iface_type = models.CharField(u'接口类型', max_length=64, choices=disk_iface_choice, default='SAS')
    memo = models.TextField(u'备注', blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    auto_create_fields = ['sn', 'slot', 'manufactory', 'model', 'capacity', 'iface_type']

    class Meta:
        unique_together = ("asset", "slot")  # 有的硬盘sn抓不到
        verbose_name = 'Disk硬盘'
        verbose_name_plural = "Disk硬盘"

    def __str__(self):
        return '%s:slot:%s capacity:%s' % (self.asset_id, self.slot, self.capacity)


class NIC(models.Model):
    """网卡组件"""

    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    name = models.CharField(u'网卡名', max_length=64, blank=True, null=True)
    sn = models.CharField(u'SN号', max_length=128, blank=True, null=True)
    macaddress = models.CharField(u'MAC', max_length=64, unique=True)

    model = models.CharField(u'网卡型号', max_length=128, blank=True, null=True)
    ipaddress = models.GenericIPAddressField(u'IP', blank=True, null=True)
    netmask = models.CharField(max_length=64, blank=True, null=True)
    bonding = models.CharField(max_length=64, blank=True, null=True)
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '%s:%s' % (self.asset_id, self.macaddress)

    class Meta:
        verbose_name = 'NIC网卡'
        verbose_name_plural = "NIC网卡"
        # unique_together = ("asset_id", "slot")
        unique_together = ("asset", "macaddress")

    auto_create_fields = ['name', 'sn', 'model', 'macaddress', 'ipaddress', 'netmask', 'bonding']


class RaidAdaptor(models.Model):
    """Raid卡"""

    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    sn = models.CharField(u'SN号', max_length=128, blank=True, null=True)
    slot = models.CharField(u'插口', max_length=64)

    model = models.CharField(u'型号', max_length=64, blank=True, null=True)
    memo = models.TextField(u'备注', blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.asset_id

    class Meta:
        unique_together = ("asset", "slot")


class Manufactory(models.Model):
    """厂商"""

    manufactory = models.CharField(u'厂商名称', max_length=64, unique=True)
    support_num = models.CharField(u'支持电话', max_length=30, blank=True)
    memo = models.CharField(u'备注', max_length=128, blank=True)

    def __str__(self):
        return self.manufactory

    class Meta:
        verbose_name = '厂商'
        verbose_name_plural = "厂商"


class BusinessUnit(models.Model):
    """业务线"""

    parent_unit = models.ForeignKey('self', on_delete=models.CASCADE, related_name='parent_level', blank=True, null=True)
    name = models.CharField(u'业务线', max_length=64, unique=True)

    memo = models.CharField(u'备注', max_length=64, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Business业务线'
        verbose_name_plural = "Business业务线"


class Contract(models.Model):
    """合同"""

    sn = models.CharField(u'合同号', max_length=128, unique=True)
    name = models.CharField(u'合同名称', max_length=64)
    memo = models.TextField(u'备注', blank=True, null=True)
    price = models.IntegerField(u'合同金额')
    detail = models.TextField(u'合同详细', blank=True, null=True)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    license_num = models.IntegerField(u'license数量', blank=True)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    class Meta:
        verbose_name = '合同'
        verbose_name_plural = "合同"

    def __str__(self):
        return self.name


class IDC(models.Model):
    """机房"""

    name = models.CharField(u'机房名称', max_length=64, unique=True)
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'IDC机房'
        verbose_name_plural = "IDC机房"


class Tag(models.Model):
    """资产标签"""

    name = models.CharField('Tag name', max_length=32, unique=True)
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Tag资产标签'
        verbose_name_plural = "Tag资产标签"


class EventLog(models.Model):
    """事件"""

    name = models.CharField(u'事件名称', max_length=100)
    event_type_choices = (
        (1, u'硬件变更'),
        (2, u'新增配件'),
        (3, u'设备下线'),
        (4, u'设备上线'),
        (5, u'定期维护'),
        (6, u'业务上线\更新\变更'),
        (7, u'其它'),
    )
    event_type = models.SmallIntegerField(u'事件类型', choices=event_type_choices)
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    component = models.CharField('事件子项', max_length=255, blank=True, null=True)
    detail = models.TextField(u'事件详情')
    date = models.DateTimeField(u'事件时间', auto_now_add=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name=u'事件源')
    memo = models.TextField(u'备注', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'EventLog事件纪录'
        verbose_name_plural = "EventLog事件纪录"

    def colored_event_type(self):
        if self.event_type == 1:
            cell_html = '<span style="background: orange;">%s</span>'
        elif self.event_type == 2:
            cell_html = '<span style="background: yellowgreen;">%s</span>'
        else:
            cell_html = '<span >%s</span>'
        return cell_html % self.get_event_type_display()

    colored_event_type.allow_tags = True
    colored_event_type.short_description = u'事件类型'


class NewAssetApprovalZone(models.Model):
    """新资产待审批区"""

    sn = models.CharField(u'资产SN号', max_length=128, unique=True)
    asset_type_choices = (
        ('server', u'服务器'),
        ('switch', u'交换机'),
        ('router', u'路由器'),
        ('firewall', u'防火墙'),
        ('storage', u'存储设备'),
        ('NLB', u'NetScaler'),
        ('wireless', u'无线AP'),
        ('software', u'软件资产'),
        ('others', u'其它类'),
    )
    asset_type = models.CharField(u'资产类型', choices=asset_type_choices, max_length=64, blank=True, null=True)
    manufactory = models.CharField(u'制造商', max_length=64, blank=True, null=True)
    model = models.CharField(u'型号', max_length=128, blank=True, null=True)
    ram_size = models.IntegerField(u'内存大小', blank=True, null=True)
    cpu_model = models.CharField(u'CPU型号', max_length=128, blank=True, null=True)
    cpu_count = models.IntegerField(u'CPU个数', blank=True, null=True)
    cpu_core_count = models.IntegerField(u'CPU核数', blank=True, null=True)
    os_distribution = models.CharField(u'系统发行版', max_length=64, blank=True, null=True)
    os_type = models.CharField(u'系统类型', max_length=64, blank=True, null=True)
    os_release = models.CharField(u'具体版本', max_length=64, blank=True, null=True)
    data = models.TextField(u'资产数据')
    date = models.DateTimeField(u'汇报日期', auto_now_add=True)
    approved = models.BooleanField(u'已批准', default=False)
    approved_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name=u'批准人', blank=True, null=True)
    approved_date = models.DateTimeField(u'批准日期', blank=True, null=True)

    def __str__(self):
        return "%s:%s" % (self.sn, self.asset_type)

    class Meta:
        verbose_name = '新上线待批准资产'
        verbose_name_plural = "新上线待批准资产"