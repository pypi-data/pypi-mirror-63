# Generated by Django 2.2.5 on 2020-01-28 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pyplan', '0016_demo_dashboards'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='my_uuid',
            field=models.UUIDField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='my_username',
            field=models.CharField(
                blank=True, default=None, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='department',
            name='company',
            field=models.ForeignKey(on_delete=models.deletion.CASCADE,
                                    related_name='departments', to='pyplan.Company'),
        ),
    ]
