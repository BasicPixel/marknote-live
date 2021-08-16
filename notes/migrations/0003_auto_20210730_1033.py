# Generated by Django 3.2.5 on 2021-07-30 07:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_alter_note_creation_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='todolist',
        ),
        migrations.AddField(
            model_name='task',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='TodoList',
        ),
    ]