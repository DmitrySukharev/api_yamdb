# Generated by Django 2.2.16 on 2022-08-12 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20220812_0840'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comments',
            options={'ordering': ('-pub_date',)},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ('-pub_date',)},
        ),
        migrations.RenameField(
            model_name='comments',
            old_name='created',
            new_name='pub_date',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='created',
            new_name='pub_date',
        ),
    ]
