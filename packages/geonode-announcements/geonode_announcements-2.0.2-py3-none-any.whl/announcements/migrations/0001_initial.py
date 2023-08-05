# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2016 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('level', models.IntegerField(default=1, choices=[(1, 'General'), (2, 'Warning'), (3, 'Critical')])),
                ('content', models.TextField(verbose_name='content')),
                ('creation_date',
                    models.DateTimeField(default=django.utils.timezone.now, verbose_name='creation_date')),
                ('site_wide', models.BooleanField(default=False, verbose_name='site wide')),
                ('members_only', models.BooleanField(default=False, verbose_name='members only')),
                ('dismissal_type',
                    models.IntegerField(
                        default=2,
                        choices=[
                            (1, 'No Dismissals Allowed'),
                            (2, 'Session Only Dismissal'),
                            (3, 'Permanent Dismissal Allowed')])),
                ('publish_start',
                    models.DateTimeField(default=django.utils.timezone.now, verbose_name='publish_start')),
                ('publish_end', models.DateTimeField(null=True, verbose_name='publish_end', blank=True)),
                ('creator', models.ForeignKey(verbose_name='creator',
                                              to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'announcement',
                'verbose_name_plural': 'announcements',
            },
        ),
        migrations.CreateModel(
            name='Dismissal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dismissed_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('announcement', models.ForeignKey(related_name='dismissals',
                                                   to='announcements.Announcement', on_delete=models.CASCADE)),
                ('user', models.ForeignKey(related_name='announcement_dismissals',
                                           to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
    ]
