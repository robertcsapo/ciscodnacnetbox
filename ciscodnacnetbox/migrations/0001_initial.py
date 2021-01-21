from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Settings",
            fields=[
                (
                    "id",
                    models.AutoField(auto_created=True, primary_key=True, serialize=False),
                ),
                ("hostname", models.CharField(max_length=2000, unique=True)),
                ("username", models.CharField(max_length=100)),
                ("password", models.CharField(max_length=100)),
                ("version", models.CharField(max_length=10)),
                ("verify", models.BooleanField(default=False)),
                ("status", models.BooleanField(default=True)),
            ],
            options={
                "ordering": ["hostname"],
            },
        ),
    ]
