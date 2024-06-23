# Generated by Django 3.2.4 on 2023-09-10 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='contactus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Query', models.CharField(max_length=100, null=True)),
                ('Name', models.CharField(max_length=200, null=True)),
                ('Email', models.CharField(max_length=100, null=True)),
                ('Mobile', models.CharField(max_length=25, null=True)),
                ('Message', models.TextField(null=True)),
            ],
        ),
    ]
