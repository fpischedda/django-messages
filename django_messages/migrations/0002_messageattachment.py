# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_messages.models


class Migration(migrations.Migration):

    dependencies = [
        ('django_messages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageAttachment',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('content', models.FileField(upload_to=django_messages.models.attachment_filename)),
                ('message', models.ForeignKey(to='django_messages.Message', related_name='message_attachment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
