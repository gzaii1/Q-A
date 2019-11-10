# Generated by Django 2.2.6 on 2019-11-07 04:42

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('question_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('question_title', models.CharField(max_length=100)),
                ('question_text', models.CharField(max_length=200)),
                ('question_type', models.CharField(default='one', max_length=50)),
                ('create_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_index', models.IntegerField(default=0)),
                ('option_val', models.CharField(default='', max_length=100)),
                ('create_time', models.DateTimeField()),
                ('correctness', models.BooleanField()),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.Question')),
            ],
        ),
    ]
