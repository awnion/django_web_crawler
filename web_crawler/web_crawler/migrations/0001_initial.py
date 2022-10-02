# Generated by Django 4.1.1 on 2022-10-02 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Crawl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('initial_url', models.URLField()),
                ('status', models.IntegerField(choices=[(0, 'PREPARE'), (1, 'RUN'), (2, 'PAUSE'), (3, 'DONE')], default=0)),
                ('strategy', models.IntegerField(choices=[(0, 'DEFAULT')], default=0)),
            ],
            options={
                'get_latest_by': 'created_at',
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('url', models.URLField()),
            ],
        ),
    ]