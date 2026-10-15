# インタフェース
# 抽象基底クラスにて、
# 全てが抽象メソッドのクラス。
# つまり、口(くち)の定義だけで、
# 実処理は一切ない。
from abc import ABC, abstractmethod

class Player(ABC):
    @abstractmethod
    def play(self):
        pass

    @abstractmethod
    def stop(self):
        pass



class MusicPlayer(Player):
    def play(self):
        print("stop")

    def stop(self):
        print('stop')

mp = MusicPlayer()
mp.play()
mp.stop()