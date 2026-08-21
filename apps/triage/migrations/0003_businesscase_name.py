from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("triage", "0002_businesscase"),
    ]

    operations = [
        migrations.AddField(
            model_name="businesscase",
            name="name",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
    ]
