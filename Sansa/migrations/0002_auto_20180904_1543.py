# Generated by Django 2.0.6 on 2018-09-04 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sansa', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='asset',
            options={'verbose_name': 'Asset资产总表', 'verbose_name_plural': 'Asset资产总表'},
        ),
        migrations.AlterModelOptions(
            name='businessunit',
            options={'verbose_name': 'Business业务线', 'verbose_name_plural': 'Business业务线'},
        ),
        migrations.AlterModelOptions(
            name='cpu',
            options={'verbose_name': 'CPU', 'verbose_name_plural': 'CPU'},
        ),
        migrations.AlterModelOptions(
            name='disk',
            options={'verbose_name': 'Disk硬盘', 'verbose_name_plural': 'Disk硬盘'},
        ),
        migrations.AlterModelOptions(
            name='eventlog',
            options={'verbose_name': 'EventLog事件纪录', 'verbose_name_plural': 'EventLog事件纪录'},
        ),
        migrations.AlterModelOptions(
            name='idc',
            options={'verbose_name': 'IDC机房', 'verbose_name_plural': 'IDC机房'},
        ),
        migrations.AlterModelOptions(
            name='networkdevice',
            options={'verbose_name': 'Network网络设备', 'verbose_name_plural': 'Network网络设备'},
        ),
        migrations.AlterModelOptions(
            name='nic',
            options={'verbose_name': 'NIC网卡', 'verbose_name_plural': 'NIC网卡'},
        ),
        migrations.AlterModelOptions(
            name='ram',
            options={'verbose_name': 'RAM内存条', 'verbose_name_plural': 'RAM内存条'},
        ),
        migrations.AlterModelOptions(
            name='server',
            options={'verbose_name': 'Server服务器', 'verbose_name_plural': 'Server服务器'},
        ),
        migrations.AlterModelOptions(
            name='software',
            options={'verbose_name': 'Software软件/系统', 'verbose_name_plural': 'Software软件/系统'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'Tag资产标签', 'verbose_name_plural': 'Tag资产标签'},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': '用户管理', 'verbose_name_plural': '用户管理'},
        ),
        migrations.AddField(
            model_name='userprofile',
            name='token',
            field=models.CharField(blank=True, default=None, max_length=128, null=True, verbose_name='token'),
        ),
    ]
