# Generated by Django 4.2 on 2023-04-20 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("captions", "0002_captionmodel_caption_model"),
    ]

    operations = [
        migrations.AddField(
            model_name="score",
            name="has_been_set",
            field=models.BooleanField(default=False),
        ),
    ]