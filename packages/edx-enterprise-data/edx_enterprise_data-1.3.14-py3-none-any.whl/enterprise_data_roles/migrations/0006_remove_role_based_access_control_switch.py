
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

ROLE_BASED_ACCESS_CONTROL_SWITCH = 'role_based_access_control'


def create_switch(apps, schema_editor):
    """Create the `role_based_access_control` switch if it does not already exist."""
    Switch = apps.get_model('waffle', 'Switch')
    Switch.objects.update_or_create(name=ROLE_BASED_ACCESS_CONTROL_SWITCH, defaults={'active': False})


def delete_switch(apps, schema_editor):
    """Delete the `role_based_access_control` switch."""
    Switch = apps.get_model('waffle', 'Switch')
    Switch.objects.filter(name=ROLE_BASED_ACCESS_CONTROL_SWITCH).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise_data_roles', '0005_turn_on_role_based_access_control_switch'),
    ]

    operations = [
        migrations.RunPython(delete_switch, create_switch),
    ]
