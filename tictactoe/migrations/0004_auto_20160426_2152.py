# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-27 00:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tictactoe', '0003_invitation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='move',
            options={'get_latest_by': 'timestamp'},
        ),
        migrations.AddField(
            model_name='move',
            name='by_first_player',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='move',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='message',
            field=models.CharField(blank=True, help_text='Adicionar uma mensagem amigável nunca é demais', max_length=300, verbose_name='Mensagem Opcional'),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='to_user',
            field=models.ForeignKey(help_text='Por favor, selecione o usuário que você quer jogar', on_delete=django.db.models.deletion.CASCADE, related_name='invitations_received', to=settings.AUTH_USER_MODEL, verbose_name='Usuário para convidar'),
        ),
    ]
