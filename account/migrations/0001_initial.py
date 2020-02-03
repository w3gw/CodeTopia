# Generated by Django 3.0.2 on 2020-02-03 11:56

import account.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(height_field=300, upload_to=account.models.get_profile_pic_path, verbose_name='Profile Picture', width_field=300)),
                ('education_background', models.CharField(choices=[('PostGraduate', 'PostGraduate'), ('UnderGraduate', 'UnderGraduate'), ('HighSchool', 'HighSchool')], max_length=30, verbose_name='Educational Background')),
                ('phone_number_1', models.CharField(max_length=13, verbose_name='First Phone Number')),
                ('phone_number_2', models.CharField(blank=True, max_length=13, null=True, verbose_name='Second Phone Number')),
                ('github_url', models.URLField(blank=True, max_length=150, null=True, verbose_name='Github homepage URL.')),
                ('personal_url', models.URLField(blank=True, max_length=150, null=True, verbose_name='Personal website URL.')),
                ('facebook_account', models.URLField(blank=True, max_length=255, null=True, verbose_name='Facebook profile page.')),
                ('twitter_account', models.URLField(blank=True, max_length=255, null=True, verbose_name='Twitter profile page.')),
                ('linkedin_account', models.URLField(blank=True, max_length=255, null=True, verbose_name='LinkedIn profile page.')),
                ('short_bio', models.CharField(blank=True, max_length=60, null=True, verbose_name='Describe yourself')),
                ('bio', models.CharField(blank=True, max_length=400, null=True, verbose_name='Short bio')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='related_user')),
            ],
            managers=[
                ('highschool', django.db.models.manager.Manager()),
            ],
        ),
    ]
