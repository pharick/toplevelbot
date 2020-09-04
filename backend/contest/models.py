from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator


class Judge(models.Model):
    telegram_username = models.CharField('Имя пользователя Telegram', max_length=32, unique=True)
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    is_doctor = models.BooleanField('Доктор', default=False)

    class Meta:
        verbose_name = 'судья'
        verbose_name_plural = 'судьи'

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Participant(models.Model):
    telegram_username = models.CharField('Имя пользователя Telegram', max_length=32, unique=True)
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    photo = models.ImageField('Фотография', upload_to='photos')
    number = models.PositiveIntegerField('Номер участника', unique=True)

    photo_lips_face_before = models.ImageField('Фото лица с губами до', upload_to='photos', blank=True)
    photo_lips_before = models.ImageField('Фото губ до', upload_to='photos', blank=True)
    photo_lips_face_after = models.ImageField('Фото лица с губами после', upload_to='photos', blank=True)
    photo_lips_after = models.ImageField('Фото губ после', upload_to='photos', blank=True)

    photo_eyeline_face_before = models.ImageField('Фото лица с веками до',upload_to='photos', blank=True)
    photo_eyeline_before = models.ImageField('Фото век до', upload_to='photos', blank=True)
    photo_eyeline_face_after = models.ImageField('Фото лица с веками после', upload_to='photos', blank=True)
    photo_eyeline_after = models.ImageField('Фото век после', upload_to='photos', blank=True)

    photo_brows_face_before = models.ImageField('Фото лица с бровями до',upload_to='photos', blank=True)
    photo_brows_before = models.ImageField('Фото бровей до', upload_to='photos', blank=True)
    photo_brows_face_after = models.ImageField('Фото лица с бровями после', upload_to='photos', blank=True)
    photo_brows_after = models.ImageField('Фото бровей после', upload_to='photos', blank=True)

    class Meta:
        verbose_name = 'участник'
        verbose_name_plural = 'участники'
        ordering = ['number']

    def __str__(self):
        return '{}: {} {}'.format(self.number, self.first_name, self.last_name)


class Rating(models.Model):
    participant = models.ForeignKey(Participant, verbose_name='Участник', on_delete=models.CASCADE)
    judge = models.ForeignKey(Judge, verbose_name='Судья', on_delete=models.CASCADE)

    CATEGORY_CHOICES = [
        (0, 'Растушевка губ'),
        (1, 'Веки с растушевкой'),
        (2, 'Пудровые брови')
    ]
    category = models.PositiveSmallIntegerField('Номинация', choices=CATEGORY_CHOICES)

    marks = ArrayField(models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)]), verbose_name="Оценки")
    message = models.TextField('Текстовый комментарий')

    class Meta:
        verbose_name = 'оценка'
        verbose_name_plural = 'оценки'

    def __str__(self):
        return 'Категория: {}; Судья: {}; Участник: {}'.format(self.category, self.judge, self.participant)


class DoctorRating(models.Model):
    participant = models.ForeignKey(Participant, verbose_name='Участник', on_delete=models.CASCADE)
    judge = models.ForeignKey(Judge, verbose_name='Судья', on_delete=models.CASCADE)

    CATEGORY_CHOICES = [
        (0, 'Растушевка губ'),
        (1, 'Веки с растушевкой'),
        (2, 'Пудровые брови')
    ]
    category = models.PositiveSmallIntegerField('Номинация', choices=CATEGORY_CHOICES)

    mark = models.SmallIntegerField(validators=[MinValueValidator(-2), MaxValueValidator(0)], verbose_name='Оценка')

    class Meta:
        verbose_name = 'оценка доктора'
        verbose_name_plural = 'оценки доктора'

    def __str__(self):
        return 'Категория: {}; Доктор: {}; Участник: {}'.format(self.category, self.judge, self.participant)


class ParticipantSession(models.Model):
    participant = models.ForeignKey(Participant, verbose_name='Участник', on_delete=models.CASCADE)
    chat_id = models.PositiveIntegerField('Идентификатор чата', unique=True)
