# Generated by Django 4.0 on 2023-08-21 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_comment', '0001_initial'),
        ('core_user', '0004_user_post_liked'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='comment_liked',
            field=models.ManyToManyField(related_name='commen_liked_by', to='core_comment.Comment'),
        ),
    ]
