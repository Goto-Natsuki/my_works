import json
import hashlib
from datetime import datetime
import pytz

class Block:
    def __init__(self, index, previous_hash, transactions=None, timestamp=None):
        # 日本標準時のタイムゾーンオブジェクトを作成
        jst = pytz.timezone('Asia/Tokyo')

        self.index = index
        self.previous_hash = previous_hash
        # トランザクションデータは要素がjsonのリスト形式
        if type(transactions)==type([]):
            self.transactions = transactions
            self.merkle_tree = self.calculate_merkle_root()
        elif type(transactions) == dict:
            self.transactions = [transactions]
            self.merkle_tree = self.calculate_merkle_root()
        elif transactions is None:
            self.transactions = []
            self.merkle_tree = 0
        self.timestamp = timestamp or datetime.now(jst)
        self.hash = self.generate_hash()

    @staticmethod
    def genesis(transactions):
        return Block(0, 0, transactions)

    def generate_hash(self):
        block_string = {
            'index': self.index,
            'previous_hash': self.previous_hash,
            'merkle_root': self.merkle_tree,
            'timestamp': self.timestamp.isoformat(),
        }
        return self.calc_hash(block_string)
    
    @staticmethod
    def calc_hash(d):
        if type(d) == dict:
            string = json.dumps(d, sort_keys=True).encode('utf-8')
        elif type(d) == type("a"):
            string = d.encode('utf-8')
        return hashlib.sha256(string).hexdigest() 

    def to_dict(self):
        return {
            'index': self.index,
            'previous_hash': self.previous_hash,
            'transactions': self.transactions,
            'timestamp': self.timestamp.isoformat(),
            'hash': self.hash,
            'merkle_tree':self.merkle_tree,
        }
    
    def calculate_merkle_root(self):
        # リーフノードのハッシュ値を計算
        hash_list = [ self.calc_hash(data)  for data in self.transactions]
        
        # 親ノードのハッシュ値を再帰的に計算
        while len(hash_list) > 1:
            if len(hash_list) % 2 == 1:
                hash_list.append(hash_list[-1])  # ツリーが奇数になる場合、最後のノードをコピーする
            hash_list = [self.calc_hash(hash_list[i] + hash_list[i+1]) 
                            for i in range(0, len(hash_list), 2)]
        
        return hash_list[0]

class Blockchain:
    def __init__(self, transactions=None, max_block_size=1000000, path=None):
        if path is not None :
            self.read_json(path)
        else:
            self.blocks = [Block.genesis(transactions=transactions)]
            self.max_block_size = max_block_size
    
    def add_block(self, transactions):
        def new_block_append(transactions):
            previous_block = self.blocks[-1]
            new_block = Block(
                index=previous_block.index+1,
                previous_hash=previous_block.hash,
                transactions=transactions
            )
            self.blocks.append(new_block)

        # データ容量を調べる
        total_size = sum(len(json.dumps(tx).encode('utf-8')) for tx in transactions)
        
        if total_size <= self.max_block_size:
            # 容量が指定値以下なら処理Aを実行
            new_block_append(transactions)
        else:
            # 容量をぎりぎり満たすトランザクションに分割してブロックをチェーンに付与する
            block_size = 0
            block_transactions = []
            for tx in transactions:
                tx_size = len(json.dumps(tx).encode('utf-8'))
                # 容量を満たさない
                if block_size + tx_size <= self.max_block_size:
                    block_transactions.append(tx)
                    block_size += tx_size
                
                # 指定容量を超えたのでブロックチェーンに付与
                else: 
                    new_block_append(block_transactions)
                    block_transactions = [tx]
                    block_size = tx_size
            
            # 最後に残ったトランザクションをチェーンに付与
            if block_transactions:
                new_block_append(block_transactions)

    def to_dict(self):
        return [block.to_dict() for block in self.blocks]

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)

    def is_chain_valid(self):
        # 対象のブロックのハッシュと1つ前のブロックのハッシュを確認
        for i in range(1, len(self.blocks)):
            current_block = self.blocks[i]
            previous_block = self.blocks[i-1]
            if current_block.previous_hash != previous_block.hash:
                return False
            if current_block.hash != current_block.calc_hash():
                return False
        return True
    
    def verify_transaction(tx_data, tx_data_tampered, root_hash):
        # マークルツリーを利用して不正なトランザクションを調査
        pass
    
    def save_json(self, path, name=None):
        if name is None:
            name = "chain_"+datetime.now().strftime("%Y%m%d_%H%M")+".json"

        with open(path+name, 'w') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False)
    
    def read_json(self, path):
        try:
            # データを読み込む
            with open(path) as f:
                self.blocks = json.load(f)

            # データが条件を満たしていない場合は、例外を発生させる
            #if not check_condition(data):
            #    raise Exception("データが条件を満たしていません。")
        except Exception as e:
            # エラーが発生した場合は、エラーメッセージを出力する
            print(f"与えられたパスからデータを読み込んだ時にエラー発生\n{e}")
    