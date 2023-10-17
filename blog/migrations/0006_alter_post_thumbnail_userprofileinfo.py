# Generated by Django 4.2.6 on 2023-10-13 01:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0005_alter_post_comments_alter_post_likes_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="thumbnail",
            field=models.ImageField(
                null=True,
                upload_to="Volumes/DATA/Python_Django/MyBlogProjec/static/images/",
            ),
        ),
        migrations.CreateModel(
            name="UserProfileInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("portfolito_site", models.URLField(blank=True)),
                ("profile_pic", models.ImageField(blank=True, upload_to="profile_pic")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="blog.user"
                    ),
                ),
            ],
        ),
    ]
