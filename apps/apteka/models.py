from django.core.validators import MinLengthValidator
from django.db import models
from ckeditor.fields import RichTextField

from apps.shared.models import AbstractBaseModel


class Type(AbstractBaseModel):
    name = models.CharField(max_length=255, verbose_name='Nomi')

    class Meta:
        db_table = 'types'
        verbose_name = 'Dori turi'
        verbose_name_plural = 'Dori turlari'

    def __str__(self):
        return self.name


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(published=True)


ranking = (
    (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)
)


class Pill(AbstractBaseModel):
    categories = models.ManyToManyField('Category', blank=True, verbose_name='Kategoriyalar')
    name = models.CharField(max_length=255, verbose_name='Nomi')
    body = RichTextField(null=True, blank=True, verbose_name="Dori haqida ma'lumot")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi")
    information = models.CharField(max_length=255, null=True, blank=True, verbose_name="Tarkibi")
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, related_name='pills', null=True, blank=True,
                             verbose_name="Dori turi")
    expiration_date = models.DateField(verbose_name="Yaroqlilik muddati")
    usage_url = models.URLField(max_length=1024, null=True, blank=True, verbose_name="Foydalanish video manzili")
    picture = models.ImageField(upload_to='pills/photos/', verbose_name="Rasmi")
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                         verbose_name="Chegirma narxi")
    published = models.BooleanField(default=False, verbose_name="Saytda ko'rinsinmi?")
    popular = models.BooleanField(default=False, verbose_name="Ommabopmi?")
    rank = models.IntegerField(choices=ranking, default=5, verbose_name="Reyting")

    objects = models.Manager()
    published_objects = PublishedManager()

    class Meta:
        db_table = 'pills'
        ordering = ["-created_at"]
        verbose_name = 'Dori'
        verbose_name_plural = 'Dorilar'

    def __str__(self):
        return f"{self.name}"


class Doctor(AbstractBaseModel):
    fullname = models.CharField(max_length=255, verbose_name="Ism-familiya")
    direction = models.CharField(max_length=255, verbose_name="Yo'nalishi")
    call = models.CharField(max_length=20, verbose_name="Telefon raqami")
    body = models.TextField(null=True, blank=True, verbose_name="Qo'shimcha ma'lumotlar")
    picture = models.ImageField(upload_to='doctors/photos/', verbose_name="Rasmi")
    advices = models.ManyToManyField(Pill, related_name='doctors', verbose_name="Tavsiya qilgan dorilari")
    published = models.BooleanField(default=False, verbose_name="Saytda ko'rinsinmi?")

    objects = models.Manager()
    published_objects = PublishedManager()

    def __str__(self):
        return self.fullname

    class Meta:
        ordering = ["-created_at"]
        db_table = 'doctors'
        verbose_name = 'Doktor'
        verbose_name_plural = 'Doktorlar'


class Partner(models.Model):
    picture = models.ImageField(upload_to='partners/photos/', verbose_name="Hamkor logosi")

    def __str__(self):
        return f"{self.picture}"

    class Meta:
        db_table = 'partners'
        ordering = ['-id']
        verbose_name = 'Hamkor'
        verbose_name_plural = 'Hamkorlar'


class Achievement(AbstractBaseModel):
    picture = models.ImageField(upload_to='achievements/images/', verbose_name="Rasmi")
    title = models.CharField(max_length=255, verbose_name="Sarlavhasi")
    description = models.CharField(max_length=255, verbose_name="Matni")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'achievements'
        ordering = ['-created_at']
        verbose_name = 'Muvaffaqiyat'
        verbose_name_plural = 'Muvaffaqiyatlar'


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nomi")

    class Meta:
        db_table = 'categories'
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'

    def __str__(self):
        return self.name


class Commentary(models.Model):
    author = models.CharField(max_length=255, verbose_name="Avtor")
    body = models.TextField(verbose_name="Izoh")
    created_at = models.DateField(auto_now_add=True, verbose_name="Izoh yozilgan vaqt")

    def __str__(self):
        return f"Commentary by {self.author} on {self.created_at}"

    class Meta:
        ordering = ["-created_at"]
        db_table = 'comments'
        verbose_name = 'Izoh'
        verbose_name_plural = 'Izohlar'


class Entry(models.Model):
    fullname = models.CharField(max_length=255, verbose_name="Ism-familiya")
    phone_number = models.CharField(max_length=20, validators=[MinLengthValidator(7)],
                                    verbose_name="Telefon raqam")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yuborilgan vaqt")

    class Meta:
        db_table = 'entries'
        ordering = ['-created_at']
        verbose_name = 'Murojat'
        verbose_name_plural = 'Murojatlar'

    def __str__(self):
        return self.fullname
