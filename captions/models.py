from django.db import models
from django.utils.html import mark_safe

# Create your models here.


class Image(models.Model):
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.image.name

    def img_preview(self):  # new
        return mark_safe(f'<img src = "{self.image.url}" width = "300"/>')


class CaptionModel(models.Model):
    name = models.CharField(max_length=200)
    comment = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Caption(models.Model):
    caption = models.CharField(max_length=200)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    model = models.ForeignKey(CaptionModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Score(models.Model):
    has_been_set = models.BooleanField(default=False)
    precision = models.IntegerField(default=5)
    recall = models.IntegerField(default=5)
    fluency = models.FloatField(default=0)
    conciseness = models.FloatField(default=0)
    inclusion = models.FloatField(default=0)
    caption = models.ForeignKey(Caption, on_delete=models.CASCADE)

    def __str__(self):
        description = (
            self.caption.caption
            + " "
            + str(self.precision)
            + " "
            + str(self.recall)
            + " "
            + str(self.fluency)
            + " "
            + str(self.conciseness)
            + " "
            + str(self.inclusion)
        )
        return description

    def img_preview(self):  # new
        return mark_safe(f'<img src = "{self.caption.image.image.url}" width = "300"/>')

    def save(self, *args, **kwargs):
        self.has_been_set = True
        super(Score, self).save(*args, **kwargs)
