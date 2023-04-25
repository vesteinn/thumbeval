from django.core.management.base import BaseCommand, CommandError
from captions.models import Caption, Score, CaptionModel, Image
from django.db.models import Avg

import collections


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass
        # parser.add_argument("file_name", type=str)
        # parser.add_argument("model", type=str)

    def handle(self, *args, **options):
        for model_prefix in ["clipcap", "blip"]:
            models = CaptionModel.objects.filter(name__startswith=model_prefix)

            for model in models:
                scores = Score.objects.filter(caption__model=model)
                precision = scores.aggregate(Avg("precision"))
                recall = scores.aggregate(Avg("recall"))
                fluency = scores.aggregate(Avg("fluency"))
                conciseness = scores.aggregate(Avg("conciseness"))
                inclusion = scores.aggregate(Avg("inclusion"))

                print("Model: ", model.name)
                print("Precision: ", precision)
                print("Recall: ", recall)
                print("Fluency: ", fluency)
                print("Conciseness: ", conciseness)
                print("Inclusion: ", inclusion)
                print("---")

            images_w_scores = Image.objects.filter(caption__score__has_been_set=True).distinct()
            binary_comp = collections.defaultdict(int)

            scores_storage = []

            for img in images_w_scores:
                captions = img.caption_set.filter(model__name__startswith=model_prefix)
                if captions.count() < 2:
                    continue

                model_result = {}

                for cap in captions:
                    score = cap.score_set.filter(has_been_set=True).first()
                    if score is None:
                        continue
                    model_result[cap.model.name] = (score.precision + score.recall) / 2

                if len(model_result) < 2:
                    continue

                vals = set(model_result.values())
                if len(vals) == 1:
                    scores_storage.append("Tie")
                    for model in model_result:
                        binary_comp[model] += 1
                else:
                    best_model = max(model_result, key=model_result.get)
                    scores_storage.append(best_model)
                    binary_comp[best_model] += 1

            print(binary_comp)
            print(f"Len scores: {len(scores_storage)}")
            ties = len([1 for x in scores_storage if x == "Tie"])
            print(f"Ties: {ties}")
            clipcap_sd = len([1 for x in scores_storage if x[-2:] == "SD"])
            print(f"SD wins: {clipcap_sd}")
            clipcap_clip = len([1 for x in scores_storage if x[-4:] == "CLIP"])
            print(f"CLIP wins: {clipcap_clip}")
            print(f"Ratio sd to clip wins: {clipcap_sd / clipcap_clip}")
            print("-----")
    