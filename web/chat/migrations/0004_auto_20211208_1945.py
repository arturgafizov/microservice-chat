# Generated by Django 3.1.7 on 2021-12-08 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_remove_chat_last_message'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ('date',)},
        ),
    ]