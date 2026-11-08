from django.shortcuts import render
from .models import Game
from .forms import GuessForm
import random

class Guess:
    def __init__(self):
        self.game = None # プレイ中のゲーム
        self.number = None # 予想した数
        self.attempts = None # 予想回数
        self.hit = None # Hit数
        self.blow = None # Blow数

    def set_hit_blow(self):

        # ヒット数（桁まで一致している数字の個数）
        self.hit = sum(1 for a, g in zip(self.game.answer, self.number) if a == g)

        # ブロウ数（桁は一致していないが正解に含まれている数字の個数）
        self.blow = sum(1 for g in self.number if g in self.game.answer) - self.hit

def create_answer():
    # ランダムな4桁の数字(重複無し)の文字列を生成
    return ''.join(map(str, random.sample(range(10), 4)))

# 中断を作ったが、うまく行かない
def index_jamp(request):
    print("satou satou")
    game = Game.objects.filter(session_id=request.session.session_key).first()
    game.is_finished = True
    game.save()
    # print(game)
    return index(request)

def index(request):
    # answer = [1,2,3,4,5]
    # guess = [4,5,6,7]
    # print(list(zip(answer, guess)))     # [(1, 4), (2, 5), (3, 6), (4, 7)]
    # for a, g in zip(answer, guess):
    #     print("a={},g={}".format(a,g))

    # セッションIDに紐づくゲームの管理情報を取得 
    game = Game.objects.filter(session_id=request.session.session_key, is_finished=False).first()

    if game is None:
        # まだゲームが開始されていない場合
        if request.session.session_key is None:
            print("game=None, kwy=None ")
            # セッションIDが送信されてきていない場合

            # セッションIDを発行
            request.session.create()

        # Gameを作成（セッションIDと紐づけ）
        # .save() を自動的に呼び出してデータベースへ保存
        game = Game.objects.create(
            answer=create_answer(), # 正解データ
            session_id=request.session.session_key # セッションID
        )
        print("create")
        # request.method = 'GET'        # satou

    guess = None
    if request.method == 'POST':
        print("post")
        # フォームからデータが送信されてきた場合 
        
        # 受信したデータからフォームを作成
        form = GuessForm(request.POST)
        if form.is_valid():
            print("form valid")
            # 受信したデータが妥当である場合

            # 予想回数をインクリメント
            game.attempts += 1

            # ユーザーが予想した数を取得
            number = form.cleaned_data['number']

            # Guessクラスのインスタンスを生成
            guess = Guess()
            guess.number = number
            guess.game = game
            guess.attempts = game.attempts

            # Hit数とBlow数を計算
            guess.set_hit_blow()

            if guess.hit == 4:
                # 予想した数が正解の場合

                # ゲーム終了フラグをセット
                game.is_finished = True

            # レコードを更新
            game.save()
        else:
            print("form invalid")
    else:
        print("not post")
        # フォームからデータが送信されてきていない場合

        # 空のフォームを生成
        form = GuessForm()


    context = {
        'game': game,
        'guess': guess,
        'form': form
    }
    return render(request, 'game/guess.html', context)