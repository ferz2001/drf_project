# Generated by Django 2.2.16 on 2021-11-10 23:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20211110_2049'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='slug',
        ),
        migrations.AddField(
            model_name='title',
            name='categorie',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='backend.Categorie'),
        ),
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default='mstTGXh4QC', max_length=20),
        ),
    ]
