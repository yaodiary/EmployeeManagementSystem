# Generated by Django 4.2.2 on 2023-06-19 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app01", "0002_alter_userinfo_create_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userinfo",
            name="create_time",
            field=models.DateField(verbose_name="入学时间"),
        ),
    ]
