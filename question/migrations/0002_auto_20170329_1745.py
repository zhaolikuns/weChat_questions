# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('question', '0001_createsuperuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('content', models.TextField(verbose_name='答案内容', max_length=1024)),
                ('is_right', models.BooleanField(verbose_name='正确答案', default=False)),
            ],
            options={
                'verbose_name': '答案',
                'verbose_name_plural': '答案',
            },
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='标题', max_length=128, default='', help_text='试卷标题, 比如 `第一学期期末测试题` 之类, 可以为空')),
                ('is_publish', models.BooleanField(verbose_name='已发布', default=False, help_text='未发布的试卷无法从前台访问作答')),
            ],
            options={
                'verbose_name': '试卷',
                'verbose_name_plural': '试卷',
            },
        ),
        migrations.CreateModel(
            name='PaperDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('paper', models.ForeignKey(related_name='detail', to='question.Paper')),
            ],
            options={
                'verbose_name': '试卷题目',
                'verbose_name_plural': '试卷题目',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.TextField(verbose_name='题目', max_length=1024)),
            ],
            options={
                'verbose_name': '题目',
                'verbose_name_plural': '题目',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('btime', models.DateTimeField(verbose_name='答题日期', auto_now_add=True)),
                ('score', models.DecimalField(verbose_name='总分', blank=True, null=True, default=None, max_digits=20, decimal_places=2)),
                ('paper', models.ForeignKey(related_name='result', to='question.Paper')),
                ('user', models.ForeignKey(related_name='score', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '答题结果',
                'verbose_name_plural': '答题结果',
                'ordering': ['-btime', 'paper', 'user'],
            },
        ),
        migrations.CreateModel(
            name='ResultDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('question_index', models.IntegerField(verbose_name='题目', help_text='题目的ID')),
                ('answer_index', models.CommaSeparatedIntegerField(verbose_name='用户提交的答案', max_length=128)),
                ('score', models.ForeignKey(related_name='detail', to='question.Result')),
            ],
        ),
        migrations.AddField(
            model_name='paperdetail',
            name='question',
            field=models.ForeignKey(verbose_name='问题', to='question.Question'),
        ),
        migrations.AddField(
            model_name='paper',
            name='question',
            field=models.ManyToManyField(related_name='paper', to='question.Question', through='question.PaperDetail'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(related_name='answer', to='question.Question'),
        ),
    ]
