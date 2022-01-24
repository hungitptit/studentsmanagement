# Generated by Django 3.2.5 on 2022-01-24 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('center', '0003_delete_excelfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('upload', models.FileField(upload_to='documents')),
            ],
        ),
        migrations.AlterField(
            model_name='result',
            name='time',
            field=models.DateTimeField(auto_now_add=True, db_column='time', max_length=255, null=True),
        ),
    ]
