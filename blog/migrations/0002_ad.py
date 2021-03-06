# Generated by Django 2.1.1 on 2018-10-15 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='广告标题')),
                ('description', models.CharField(max_length=200, verbose_name='广告描述')),
                ('image_url', models.ImageField(upload_to='ad/%Y/%m', verbose_name='图片路径')),
                ('callback_url', models.URLField(blank=True, null=True, verbose_name='回调url')),
                ('date_publish', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('index', models.IntegerField(default=999, verbose_name='排列顺序(从小到大)')),
            ],
            options={
                'verbose_name': '广告',
                'verbose_name_plural': '广告',
                'ordering': ['index', 'id'],
            },
        ),
    ]
