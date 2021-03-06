# Generated by Django 3.0.3 on 2020-03-30 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orchestrator', '0007_v030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalscheduletrigger',
            name='next_execution',
            field=models.DateTimeField(blank=True, editable=False, help_text='This field specifies the scheduled time for the next execution.', null=True),
        ),
        migrations.AlterField(
            model_name='scheduletrigger',
            name='next_execution',
            field=models.DateTimeField(blank=True, editable=False, help_text='This field specifies the scheduled time for the next execution.', null=True),
        ),
    ]
