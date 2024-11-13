# Generated by Django 2.0.3 on 2021-03-28 08:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback_Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('mobilenumber', models.CharField(max_length=100)),
                ('feedback', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='TweetModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tweet', models.CharField(max_length=500)),
                ('topics', models.CharField(max_length=300)),
                ('sentiment', models.CharField(max_length=300)),
                ('images', models.FileField(upload_to='')),
                ('age', models.CharField(max_length=500)),
                ('transport', models.CharField(max_length=500)),
                ('time', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Userregister_Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=30)),
                ('password', models.CharField(max_length=10)),
                ('phoneno', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=500)),
                ('dob', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=30)),
                ('bad', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='tweetmodel',
            name='userId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Client.Userregister_Model'),
        ),
    ]