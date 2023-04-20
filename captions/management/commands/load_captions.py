from django.core.management.base import BaseCommand, CommandError
from captions.models import Caption, Score, CaptionModel, Image


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("file_name", type=str)
        parser.add_argument("model", type=str)

    def handle(self, *args, **options):
        clip_model, _ = CaptionModel.objects.get_or_create(
            name=options["model"] + "_CLIP"
        )
        sd_model, _ = CaptionModel.objects.get_or_create(name=options["model"] + "_SD")

        with open(options["file_name"], "r") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip().split("\t")
                image_name = line[0].split("/")[-1]
                clip_caption = line[4]
                sd_caption = line[5]

                img = Image.objects.create(image=image_name)
                sd_caption = Caption.objects.create(
                    caption=sd_caption, image=img, model=sd_model
                )
                clip_caption = Caption.objects.create(
                    image=img, model=clip_model, caption=clip_caption
                )

                Score.objects.create(caption=sd_caption)
                Score.objects.create(caption=clip_caption)
