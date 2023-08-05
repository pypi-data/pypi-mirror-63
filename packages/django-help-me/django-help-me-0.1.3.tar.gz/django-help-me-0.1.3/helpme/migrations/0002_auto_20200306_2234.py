# Generated by Django 2.2.4 on 2020-03-06 22:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('helpme', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supportrequest',
            name='assignees',
            field=models.ManyToManyField(blank=True, related_name='support_request_assignments', to=settings.AUTH_USER_MODEL, verbose_name='Asignees'),
        ),
        migrations.AlterField(
            model_name='supportrequest',
            name='category',
            field=models.IntegerField(choices=[(1, 'Comment'), (2, 'Sales'), (3, 'Help'), (4, 'Bug')], default=10, verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='supportrequest',
            name='status',
            field=models.IntegerField(choices=[(1, 'Open'), (10, 'Active'), (20, 'Hold'), (30, 'Closed'), (40, 'Canceled')], default=1, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='supportrequest',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='support_request', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='SupportEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='last updated')),
                ('description', models.TextField(verbose_name='Description')),
                ('visibility', models.IntegerField(choices=[(1, 'Reporters'), (10, 'Support Handlers'), (20, 'Supervisors')], default=1, verbose_name='Visibility')),
                ('category', models.IntegerField(choices=[(1, 'Logged Event'), (10, 'Note'), (20, 'Reply')], default=1, verbose_name='Category')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='support_events', to='helpme.SupportRequest', verbose_name='Support Event')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
