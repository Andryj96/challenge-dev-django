# Generated by Django 4.2 on 2023-06-18 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0003_alter_proposalfield_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposalfieldvalue',
            name='value',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
