# Generated by Django 3.2.5 on 2022-01-31 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('center', '0002_alter_result_testid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='classid',
            field=models.ForeignKey(db_column='ClassID', on_delete=django.db.models.deletion.CASCADE, to='center.class'),
        ),
    ]
