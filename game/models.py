from django.db import models

class Game(models.Model):
    answer = models.CharField(max_length=4) # 正解
    attempts = models.IntegerField(default=0) # 予想回数
    is_finished = models.BooleanField(default=False) # ゲームクリアフラグ
    session_id = models.CharField(max_length=40) # セッションID