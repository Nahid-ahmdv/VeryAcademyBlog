# Generated by Django 3.0.8 on 2024-10-23 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='blog.Category'),
        ),
    ]