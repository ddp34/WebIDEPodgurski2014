# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_ide', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=1, choices=[(b's', b'system'), (b'a', b'action'), (b'm', b'message'), (b'j', b'join'), (b'l', b'leave'), (b'n', b'notification')])),
                ('sender', models.CharField(max_length=50, blank=True)),
                ('message', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
