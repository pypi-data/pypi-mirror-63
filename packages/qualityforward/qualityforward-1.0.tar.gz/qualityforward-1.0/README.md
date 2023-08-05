# QualityForward用Pythonライブラリ

## 使い方

```py
from qualityforward.QualityForward import QualityForward

if __name__ == '__main__':
    q = QualityForward("0aa...340") # APIキー
    print(q.get_current_project().name) # -> サンプルプロジェクト
```

## LICENSE

MIT
