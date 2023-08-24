# Generated by Django 4.0 on 2023-08-10 15:02

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core_user', '0004_user_post_liked'),
        ('core_post', '0003_alter_post_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('body', models.TextField()),
                ('edited', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core_user.user')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core_post.post')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
