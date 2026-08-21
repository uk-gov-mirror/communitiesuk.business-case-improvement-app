from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("triage", "0004_businesscase_directorate_businesscase_lead_contact_and_more"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql="""
                        CREATE TYPE business_case_status AS ENUM (
                            'Active', 'Uploaded', 'Withdrawn'
                        );
                        UPDATE triage_businesscase
                        SET status = 'Active'
                        WHERE status = '';
                        ALTER TABLE triage_businesscase
                        ALTER COLUMN status TYPE business_case_status
                        USING status::business_case_status;
                    """,
                    reverse_sql="""
                        ALTER TABLE triage_businesscase
                        ALTER COLUMN status TYPE varchar(255)
                        USING status::text;
                        DROP TYPE business_case_status;
                    """,
                ),
            ],
            state_operations=[
                migrations.AlterField(
                    model_name="businesscase",
                    name="status",
                    field=models.CharField(
                        choices=[
                            ("Active", "Active"),
                            ("Uploaded", "Uploaded"),
                            ("Withdrawn", "Withdrawn"),
                        ],
                        default="Active",
                        max_length=9,
                    ),
                ),
            ],
        ),
    ]
