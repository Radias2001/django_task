from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse, NoReverseMatch

class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200, blank=True)
    named_url = models.CharField(max_length=100, blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    def get_url(self) -> str:
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                return '#'
        return self.url or '#'

    def clean(self):
        super().clean()

        if self.parent:
            if self.parent == self:
                raise ValidationError("Элемент не может быть родителем сам себе.")

            ancestor = self.parent
            while ancestor:
                if ancestor == self:
                    raise ValidationError("Обнаружено зацикливание в структуре меню.")
                ancestor = ancestor.parent

        if self.url and self.named_url:
            raise ValidationError("Укажите либо 'URL', либо 'Named URL', но не и то и то.")

        if not self.url and not self.named_url:
            raise ValidationError("Нужно указать либо 'URL', либо 'Named URL'.")



    def __str__(self):
        return self.title
