from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
    ]
    operations = [
        migrations.CreateModel(
            name="Settings",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ("hostname", models.CharField(max_length=2000, unique=True)),
                ("username", models.CharField(max_length=100)),
                ("password", models.CharField(max_length=100)),
                ("version", models.CharField(max_length=10)),
                ("verify", models.BooleanField(default=False)),
                ("status", models.BooleanField(default=True)),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, blank=True, null=True),
                ),
                (
                    "last_updated",
                    models.DateTimeField(auto_now_add=True, blank=True, null=True),
                ),
            ],
            options={
                "app_label": "ciscodnacnetbox",
                "ordering": ["hostname"],
            },
        ),
    ]
