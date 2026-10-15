# インタフェース
# 抽象基底クラスにて、
# 全てが抽象メソッドのクラス。
# つまり、口(くち)の定義だけで、
# 実処理は一切ない。
from abc import ABC, abstractmethod

class Player(ABC):