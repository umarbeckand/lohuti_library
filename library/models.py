from django.db import models


class Author(models.Model):
    """Модель автора книги"""
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=100, blank=True, verbose_name='Отчество')
    slug = models.SlugField(unique=True, verbose_name='URL')
    biography = models.TextField(blank=True, verbose_name='Биография')
    birth_year = models.IntegerField(null=True, blank=True, verbose_name='Год рождения')
    death_year = models.IntegerField(null=True, blank=True, verbose_name='Год смерти')
    photo = models.ImageField(upload_to='authors/', blank=True, verbose_name='Фото')
    
    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"
    
    def get_full_name(self):
        return self.__str__()


class Category(models.Model):
    """Категория книги"""
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Описание')
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Book(models.Model):
    """Модель книги"""
    STATUS_CHOICES = [
        ('available', 'Доступна'),
        ('borrowed', 'Выдана'),
        ('reserved', 'Зарезервирована'),
        ('maintenance', 'На обслуживании'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL')
    authors = models.ManyToManyField(Author, related_name='books', verbose_name='Авторы')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='books', verbose_name='Категория')
    isbn = models.CharField(max_length=17, blank=True, verbose_name='ISBN')
    description = models.TextField(blank=True, verbose_name='Описание')
    publisher = models.CharField(max_length=200, blank=True, verbose_name='Издательство')
    publication_year = models.IntegerField(null=True, blank=True, verbose_name='Год издания')
    pages = models.IntegerField(null=True, blank=True, verbose_name='Количество страниц')
    language = models.CharField(max_length=50, default='Тоҷикӣ', verbose_name='Язык')
    cover_image = models.ImageField(upload_to='books/covers/', blank=True, verbose_name='Обложка')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name='Статус')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество экземпляров')
    available_quantity = models.PositiveIntegerField(default=1, verbose_name='Доступно экземпляров')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлена')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлена')
    
    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def is_available(self):
        return self.available_quantity > 0


class News(models.Model):
    """Новости библиотеки"""
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, verbose_name='URL')
    content = models.TextField(verbose_name='Содержание')
    image = models.ImageField(upload_to='news/', blank=True, verbose_name='Изображение')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-published_at']
    
    def __str__(self):
        return self.title


class Event(models.Model):
    """Мероприятия библиотеки"""
    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='events/', blank=True, verbose_name='Изображение')
    event_date = models.DateTimeField(verbose_name='Дата мероприятия')
    location = models.CharField(max_length=200, verbose_name='Место проведения')
    is_active = models.BooleanField(default=True, verbose_name='Активно')
    
    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        ordering = ['-event_date']
    
    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    """Сообщения от посетителей"""
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email')
    subject = models.CharField(max_length=200, verbose_name='Тема')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
