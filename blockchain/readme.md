# Blockchain
これはPythonによるブロックチェーンの簡単な実装です。このコードには2つのクラスが含まれています。BlockとBlockchainです。

## Blockクラス
Block クラスは、ブロックチェーンにおけるブロックを表します。

### 属性

- index: ブロックチェーンにおけるブロックのインデックス。
- previous_hash：ブロックチェーン内の前のブロックのハッシュ。
- transactions：ブロックに含まれるトランザクションのリスト。
- merkle_tree: トランザクションのMerkleツリールート。
- timestamp：ブロックが作成された時のタイムスタンプ。
- hash：ブロックのハッシュ。

### メソッド

- \_\_init\_\_()：ブロックの属性を初期化するコンストラクタ・メソッド。
- generate_hash()：ブロックのハッシュを SHA-256 アルゴリズムで生成する。
- to_dict()：ブロックを辞書として返す。
- calculate_merkle_root()：トランザクションのMerkleツリーのルートを計算する。


## Blockchainクラス
Blockchain クラスは、ブロックチェーンそのものを表します。

### 属性

- blocks: ブロックチェーンに含まれるブロックのリスト。
- max_block_size: ブロックの最大サイズ（バイト単位）。

### メソッド

- \_\_init\_\_()：ブロックチェーンをジェネシスブロックで初期化するコンストラクタ・メソッド。
- add_block()：与えられたトランザクションを持つブロックをブロックチェーンに追加します。
- to_dict()：ブロックチェーンを辞書のリストとして返します。ブロックチェーンをJSON文字列として返す。
- is_chain_valid()：ブロックチェーンが有効かどうかチェックする。
- verify_transaction()：まだ未完。
- read_json()：引数にパスを取ることでjsonを読み込める。ただし、内容が本クラスにそっているかどうかを判断する機能は未実装。

```python
from datetime import datetime

data1 = {
  "name": "山田太郎",
  "age":     25,
  "address": "東京都渋谷区",
  "timestamp": datetime.now().strftime("%Y/%m/%d %H:%M:%S")
}

data2 = {
  "name": "田中花子",
  "age":     30,
  "address": "大阪府大阪市",
  "timestamp": datetime.now().strftime("%Y/%m/%d %H:%M:%S")
}

data3 = {
  "name": "鈴木次郎",
  "age":     40,
  "address": "愛知県名古屋市",
  "timestamp": datetime.now().strftime("%Y/%m/%d %H:%M:%S")
}

# データをリストに格納
json_data = [data1, data2, data3]

# 初めのjsonデータを格納
chain = Blockchain(transactions=json_data[0])

# 残りのjsonデータを格納
chain.add_block(json_data[1:])

# blockchainの全体表示
print(chain.to_dict())

```

# 注意
 
まだ未完成の部分があるのでご注意ください。
 
# 作成者
 
goto natsuki
 
# License

このモジュールは[MIT license](https://en.wikipedia.org/wiki/MIT_License)です.