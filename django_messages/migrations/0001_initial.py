# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('subject', models.CharField(max_length=120, verbose_name='Subject')),
                ('body', models.TextField(verbose_name='Body')),
                ('sent_at', models.DateTimeField(auto_now_add=True, verbose_name='sent at')),
                ('read_at', models.DateTimeField(verbose_name='read at', blank=True, null=True)),
                ('replied_at', models.DateTimeField(verbose_name='replied at', blank=True, null=True)),
                ('sender_deleted_at', models.DateTimeField(verbose_name='Sender deleted at', blank=True, null=True)),
                ('recipient_deleted_at', models.DateTimeField(verbose_name='Recipient deleted at', blank=True, null=True)),
                ('parent_msg', models.ForeignKey(to='django_messages.Message', blank=True, related_name='next_messages', null=True, verbose_name='Parent message')),
                ('recipient', models.ForeignKey(related_name='received_messages', to=settings.AUTH_USER_MODEL, verbose_name='Recipient')),
                ('sender', models.ForeignKey(related_name='sent_messages', to=settings.AUTH_USER_MODEL, verbose_name='Sender')),
            ],
            options={
                'ordering': ['-sent_at'],
                'verbose_name_plural': 'Messages',
                'verbose_name': 'Message',
            },
            bases=(models.Model,),
        ),
    ]
