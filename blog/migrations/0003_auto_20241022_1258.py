# Generated by Django 3.0.8 on 2024-10-22 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20241019_1408'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-publish_date',)},
        ),
        migrations.AddField(
            model_name='post',
            name='excerpt',
            field=models.TextField(null=True),
        ),
    ]
