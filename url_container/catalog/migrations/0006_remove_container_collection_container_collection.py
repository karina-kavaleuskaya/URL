# Generated by Django 5.0.4 on 2024-04-18 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_alter_container_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='container',
            name='collection',
        ),
        migrations.AddField(
            model_name='container',
            name='collection',
            field=models.ManyToManyField(blank=True, null=True, to='catalog.collection'),
        ),
    ]