# Generated by Django 4.0.3 on 2022-06-03 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendees', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountVO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(null=True)),
                ('updated', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
