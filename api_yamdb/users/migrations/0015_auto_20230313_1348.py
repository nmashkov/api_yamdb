# Generated by Django 3.2 on 2023-03-13 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_alter_user_role'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.RemoveField(
            model_name='user',
            name='confirmation_code',
        ),
    ]