# mergekit-evolve-elyzatask100

## 参照
うみゆき先生、npaka先生のコードを参照しています。  
 - [Mergekit-Evolve登場！進化的アルゴリズムで手元のLLMを最強進化させよう！](https://soysoftware.sakura.ne.jp/archives/3872)
 - [Google Colab で mergekit-evolve による 進化的モデルマージ を試す](https://note.com/npaka/n/n42129c043026?sub_rt=share_h)

## Google Colabでの使用方法
### パッケージのインストール
```
# パッケージのインストール
!git clone --recurse-submodules https://github.com/Hajime-Y/mergekit-evolve-elyzatask100.git
%cd mergekit-evolve-elyzatask100/mergekit
!cp ../evol_merge_config.yaml ./
!pip install -e .[evolve]
```

### 設定の確認（マージするモデル、マージ方法等はここで変更する）
```
# 設定の確認（マージするモデル、マージ方法等はここで変更する）
!cat evol_merge_config.yaml
```

### 環境変数の準備
```
import os
from huggingface_hub import login
from google.colab import userdata

# GeminiのAPI Keyの設定（左端の鍵アイコンでGOOGLE_API_KEYを設定）
os.environ["GOOGLE_API_KEY"] = userdata.get("GOOGLE_API_KEY")

# HuggingFaceログイン（左端の鍵アイコンでHF_TOKENを設定）
login(userdata.get("HF_TOKEN"))
```

### 進化的マージの実行
```
# マージの実行
!mergekit-evolve ./evol_merge_config.yaml \
    --storage-path ../evol_merge_storage \
    --task-search-path ../eval_tasks \
    --in-memory \
    --merge-cuda \
    --wandb
```

### 最終モデルの生成とHuggingFaceへの保存
```
# 最終モデルの生成
!mergekit-yaml ../evol_merge_storage/best_config.yaml --cuda ../final_merge

# HuggingFaceへの保存
!huggingface-cli upload HachiML/Swallow-MS-7b-MergeEvol-fevals105 ../final_merge .
```

## 前提
 - このコードはGoogleのGemini ProのAPI Keyが必要です。Gemini ProのAPI Keyは[Google AI Studio](https://aistudio.google.com/app/apikey)から取得が可能です。