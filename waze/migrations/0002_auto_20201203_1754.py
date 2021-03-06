# Generated by Django 2.2.17 on 2020-12-03 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('waze', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='number_of_visit',
            field=models.IntegerField(blank=True, null=True, verbose_name='Number of store'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='restau_img_url',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='restau_type',
            field=models.IntegerField(choices=[(1, 'Breakfast'), (2, 'Lunch'), (3, 'Dinner'), (4, 'Cafe'), (5, 'Buffet'), (6, 'Fine Dining')], default=1),
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name of the menu')),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, default=1.0, max_digits=10)),
                ('img_url', models.TextField(blank=True, null=True)),
                ('is_specialty', models.BooleanField(default=False)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='waze.Restaurant')),
            ],
        ),
    ]
