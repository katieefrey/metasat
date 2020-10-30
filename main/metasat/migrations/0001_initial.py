# Generated by Django 3.0.7 on 2020-10-29 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ElementFamily',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('family', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('segment', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=255, unique=True)),
                ('term', models.CharField(max_length=255)),
                ('synonym', models.CharField(blank=True, max_length=255, null=True)),
                ('example', models.TextField(blank=True, null=True)),
                ('desc', models.TextField(blank=True, null=True)),
                ('source', models.TextField(blank=True, null=True)),
                ('deprecated', models.BooleanField(default=False)),
                ('deprecatedon', models.DateField(blank=True, null=True)),
                ('family', models.ManyToManyField(blank=True, to='metasat.ElementFamily')),
                ('mapping', models.ManyToManyField(blank=True, related_name='_element_mapping_+', to='metasat.Element')),
                ('segment', models.ManyToManyField(blank=True, to='metasat.Segment')),
            ],
            options={
                'ordering': ('identifier',),
            },
        ),
    ]
