# Generated by Django 3.2 on 2023-03-10 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(
                blank=True,
                choices=[(1, 'admin'), (2, 'moderator'), (3, 'user')],
                default=3,
                verbose_name='Роль'),
        ),
    ]
