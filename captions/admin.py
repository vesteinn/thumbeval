from django.contrib import admin

from .models import Caption, Image, Score, CaptionModel

# Register your models here.
admin.site.register(CaptionModel)


class ScoreInline(admin.TabularInline):
    model = Score
    extra = 0


class CaptionInline(admin.TabularInline):
    model = Caption
    extra = 0


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    inlines = [CaptionInline]
    readonly_fields = ["img_preview"]
    list_display = ["img_preview"]


@admin.register(Caption)
class CaptionAdmin(admin.ModelAdmin):
    inlines = [ScoreInline]
    list_display = ["caption", "image", "model"]


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display_links = None
    list_display = [
        "caption_model",
        "has_been_set",
        "img_preview",
        "caption",
        "precision",
        "recall",
        "fluency",
        "conciseness",
        "inclusion",
    ]
    list_editable = [
        "has_been_set",
        "precision",
        "recall",
        "fluency",
        "conciseness",
        "inclusion",
    ]
    list_filter = ["has_been_set", "caption__model"]

    def caption_model(self, obj):
        return obj.caption.model
