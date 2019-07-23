import uuid

from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel


class AccessLevel(TimeStampedModel):
    """
    Level of permission
    """
    name = models.CharField(max_length=55, verbose_name='Название уровня')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Уровень'
        verbose_name_plural = 'Уровни'


class Permit(TimeStampedModel):
    """
    Permission
    """
    NOT_ACTIVE = 0
    ACTIVE = 1
    EXPIRED = 2
    BLOCKED = 3

    STATUS_TYPES = (
        (NOT_ACTIVE, 'Не активен'),
        (ACTIVE, 'Активный'),
        (EXPIRED, 'Просрочен'),
        (BLOCKED, 'Заблокирован')
    )

    number = models.CharField(max_length=25, verbose_name='Номер пропуска')
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    date_from = models.DateTimeField(verbose_name='От', help_text='Срок годности (от)')
    date_to = models.DateTimeField(verbose_name='До', help_text='Срок годности (до)')
    level = models.ForeignKey(AccessLevel, on_delete=models.CASCADE, verbose_name='Уровень доступа')
    status = models.PositiveIntegerField(default=ACTIVE, choices=STATUS_TYPES, verbose_name='Статус')

    def __str__(self):
        return '{}'.format(self.number)

    class Meta:
        verbose_name = 'Пропуск'
        verbose_name_plural = 'Пропуски'


class Person(TimeStampedModel):
    """
    Employee
    """
    NOT_ACTIVE = 0
    ACTIVE = 1
    EXPIRED = 2
    IN_PROCESS = 3

    STATUS_TYPES = (
        (NOT_ACTIVE, 'Не активен'),
        (IN_PROCESS, 'На рассмотрении'),
        (ACTIVE, 'Активный'),
        (EXPIRED, 'Просрочен документ')
    )
    first_name = models.CharField(max_length=55, verbose_name='Имя')
    last_name = models.CharField(max_length=55, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=55, blank=True, verbose_name='Отчество')
    position = models.CharField(max_length=255, verbose_name='Должность')
    contractor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Подрядчик')
    permit = models.ForeignKey(Permit, null=True, blank=True, on_delete=models.SET_NULL,
                               verbose_name='Пропуск')
    status = models.PositiveIntegerField(default=NOT_ACTIVE, choices=STATUS_TYPES, verbose_name='Статус')

    def edit_url(self):
        return "/lk/person/{}/".format(self.id)

    def add_doc_url(self):
        return "/lk/person/{}/add_doc".format(self.id)

    def __str__(self):
        return '{} {}'.format(self.last_name, self.first_name)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class TypeDocument(TimeStampedModel):
    """
    Type of document
    """
    name = models.CharField(max_length=255, verbose_name='Название типа')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Тип документа'
        verbose_name_plural = 'Тип документов'


class Document(TimeStampedModel):
    """
    Document
    """
    NEW = 0
    CHECKED = 1
    CANCELLED = 2
    STATUS_TYPES = (
        (NEW, 'Новый'),
        (CHECKED, 'Проверен'),
        (CANCELLED, 'Отклонён')
    )

    person = models.ForeignKey(Person, related_name='documents', on_delete=models.CASCADE, verbose_name='Сотрудник')
    type_doc = models.ForeignKey(TypeDocument, on_delete=models.CASCADE, verbose_name='Тип документа')
    date_from = models.DateTimeField(blank=True, verbose_name='Срок действия (от)', help_text='Дата и время (от)')
    date_to = models.DateTimeField(blank=True, verbose_name='Срок действия (до)', help_text='Дата и время (до)')
    file = models.FileField(upload_to='uploads/documents/', verbose_name='Файл', help_text='Загрузите скан документа')
    status = models.PositiveIntegerField(default=0, choices=STATUS_TYPES, verbose_name='Статус')

    def __str__(self):
        return '{}'.format(self.type_doc)

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'


class EquipmentType(TimeStampedModel):
    """
    Equipment Type
    """
    name = models.CharField(max_length=255, verbose_name='Название типа')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Тип оборудования'
        verbose_name_plural = 'Типы оборудования'


class Equipment(TimeStampedModel):
    """
    Equipment
    """
    NOT_CHECKED = 0
    CHECKED = 1
    CANCELLED = 2
    ACCESS_TYPES = (
        (NOT_CHECKED, 'Не проверено'),
        (CHECKED, 'Проверен'),
        (CANCELLED, 'Отклонён')
    )

    person = models.ForeignKey(Person, null=True, on_delete=models.CASCADE, verbose_name='Сотрудник')
    type_eq = models.ForeignKey(EquipmentType, on_delete=models.CASCADE, verbose_name='Тип оборудования')
    number = models.CharField(max_length=255, verbose_name='Номер')
    access = models.PositiveIntegerField(default=NOT_CHECKED, choices=ACCESS_TYPES, verbose_name='Разрешение')

    def __str__(self):
        return '{}'.format(self.type_eq)

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'


class Event(TimeStampedModel):
    """
    Event
    """
    NEW = 0
    CHECKED = 1
    CANCELLED = 2
    STATUS_TYPES = (
        (NEW, 'Новое'),
        (CHECKED, 'Выполнено'),
        (CANCELLED, 'Отклонёно')
    )

    CHANGES_DATA = 0
    REQUEST_PERMIT = 1
    EVENT_TYPES = (
        (CHANGES_DATA, 'Изменение данных'),
        (REQUEST_PERMIT, 'Запрос пропуска')
    )

    event_type = models.PositiveIntegerField(default=CHANGES_DATA, choices=EVENT_TYPES, verbose_name='Тип события')
    persons = models.ManyToManyField(Person, verbose_name='Сотрудники')
    status = models.PositiveIntegerField(default=NEW, choices=STATUS_TYPES, verbose_name='Статус')

    def __str__(self):
        return '{}'.format(self.get_event_type_display())

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
