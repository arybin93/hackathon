# Generated by Django 2.2.3 on 2019-07-21 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20190721_0350'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='person',
        ),
        migrations.AddField(
            model_name='event',
            name='persons',
            field=models.ManyToManyField(to='app.Person', verbose_name='Сотрудники'),
        ),
        migrations.AlterField(
            model_name='document',
            name='date_from',
            field=models.DateTimeField(blank=True, help_text='Дата и время (от)', verbose_name='Срок действия (от)'),
        ),
        migrations.AlterField(
            model_name='document',
            name='date_to',
            field=models.DateTimeField(blank=True, help_text='Дата и время (до)', verbose_name='Срок действия (до)'),
        ),
        migrations.AlterField(
            model_name='document',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='app.Person', verbose_name='Сотрудник'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.PositiveIntegerField(choices=[(0, 'Изменение данных'), (1, 'Запрос пропуска')], default=0, verbose_name='Тип события'),
        ),
        migrations.AlterField(
            model_name='person',
            name='status',
            field=models.PositiveIntegerField(choices=[(0, 'Не активен'), (3, 'В процессе'), (1, 'Активный'), (2, 'Просрочен документ')], default=0, verbose_name='Статус'),
        ),
    ]