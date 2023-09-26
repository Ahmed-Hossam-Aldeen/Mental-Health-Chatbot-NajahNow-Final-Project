# Generated by Django 4.1 on 2022-09-03 21:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("user_id", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=30)),
                ("email", models.EmailField(max_length=254)),
                ("passwrd", models.CharField(max_length=20)),
                ("age", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Messege",
            fields=[
                ("msg_id", models.IntegerField(primary_key=True, serialize=False)),
                ("msg_ord", models.IntegerField(verbose_name=1)),
                ("messege", models.CharField(max_length=1000)),
                ("by_user", models.BinaryField(default=0)),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="rasaweb.user"
                    ),
                ),
            ],
        ),
    ]
