# Generated by Django 2.2.6 on 2019-10-23 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BackTrack', '0006_project_product_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='productbacklog',
            name='sprint',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sprint', to='BackTrack.SprintBacklog'),
        ),
    ]
