# Generated by Django 4.2.15 on 2024-08-20 10:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('books', '0005_remove_summary_book_summary_book_title'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Audiobook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio_file', models.FileField(upload_to='audiobooks/')),
                ('duration', models.DurationField()),
                ('is_available', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('narrator', models.CharField(blank=True, max_length=255, null=True, verbose_name='narrator')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audiobooks', to='books.book')),
            ],
        ),
        migrations.CreateModel(
            name='Download',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('downloaded_at', models.DateTimeField(auto_now_add=True)),
                ('audiobook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audiobooks.audiobook')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
