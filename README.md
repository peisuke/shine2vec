# 社員2vec

# How to use

## 必須モジュールをインストール

```
pip install -r requirements.txt
```

## Slackからの会話履歴ダウンロード

2ヶ月分の会話履歴のダウンロードをする。1時間ほど掛かるので気長に待つ。

```
SLACK_TOKEN=XXXXXXXXXXXXXXXXX python download.py
```

## 社員2vecの学習

社員ベクトルの学習

```
python train.py
```

## 類似社員の検索

```
python most_similar.py --target [user name]
```

## 社員の相関マップ表示

```
python plot_relationship.py
```

![image](https://user-images.githubusercontent.com/14243883/70375683-01fc3d80-1944-11ea-9fdd-c6525f646d13.png)

> 日本語が文字化けを起こす場合は[こちら](https://datumstudio.jp/blog/matplotlibの日本語文字化けを解消するwindows編)を参照

## 社員を別の社員の線形和で再構成

```
python predict.py --target [user name]
```
