# Generated by Django 4.2.7 on 2023-11-29 10:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("workers", "0003_alter_worker_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="worker",
            name="is_published",
            field=models.BooleanField(
                choices=[(0, "Черновик"), (1, "Опубликовано")], default=0
            ),
        ),
    ]
