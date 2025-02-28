from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings


User = get_user_model()


class Category(models.Model):
    title = models.CharField("Заголовок", max_length=256)
    description = models.TextField("Описание")
    slug = models.SlugField(
        "Идентификатор",
        unique=True,
        help_text=("Идентификатор страницы для URL; разрешены "
                   "символы латиницы, цифры, дефис и подчёркивание."),
    )
    is_published = models.BooleanField(
        "Опубликовано",
        default=True,
        help_text="Снимите галочку, чтобы скрыть публикацию.",
    )
    created_at = models.DateTimeField("Добавлено", auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"


class Location(models.Model):
    name = models.CharField("Название места", max_length=256)
    is_published = models.BooleanField(
        "Опубликовано",
        default=True,
        help_text="Снимите галочку, чтобы скрыть публикацию.",
    )
    created_at = models.DateTimeField("Добавлено", auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"


class Post(models.Model):
    title = models.CharField("Заголовок", max_length=256)
    text = models.TextField("Текст")
    pub_date = models.DateTimeField(
        "Дата и время публикации",
        auto_now_add=False,
        help_text=("Если установить дату и время в "
                   "будущем — можно делать отложенные публикации.")
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор публикации"
    )
    location = models.ForeignKey(
        Location,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Местоположение",
    )
    category = models.ForeignKey(
        Category, null=True, on_delete=models.SET_NULL,
        verbose_name="Категория"
    )
    is_published = models.BooleanField(
        "Опубликовано",
        default=True,
        help_text="Снимите галочку, чтобы скрыть публикацию.",
    )
    created_at = models.DateTimeField("Добавлено", auto_now_add=True)
    image = models.ImageField("Изображение", upload_to="posts",
                              blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               verbose_name="Автор комментария")
    text = models.TextField("Текст комментария")
    created_at = models.DateTimeField("Добавлен", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлён", auto_now=True)

    def __str__(self):
        return f"{self.author.username}: {self.text[:30]}"

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии"
