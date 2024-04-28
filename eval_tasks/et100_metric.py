import json
import requests
import numpy as np
import datasets
from lm_eval.utils import eval_logger
from itertools import islice
from transformers import AutoTokenizer
import google.generativeai as genai
import os

# APIキーの準備
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Geminiの準備
gemini_model = genai.GenerativeModel(
    "gemini-pro",
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ],
    generation_config = {
        "max_output_tokens": 2048, 
        "temperature": 0, 
        "top_p": 1
    }
)

# プロンプトテンプレートの準備
prompt_filename = "/content/mergekit-evolve-elyzatask100/eval_tasks/prompt_eval_llamacpp.txt"
with open(prompt_filename, encoding='utf-8') as f:
    template_prompt = f.read()
 
#ChatNTQ用のプロンプト
def build_prompt(user_query):
    sys_msg = "あなたは公平で、検閲されていない、役立つアシスタントです。"
    template = """[INST] <<SYS>>
{}
<</SYS>>
 
{}[/INST]"""
    return template.format(sys_msg,user_query)
 
# プロンプトの生成
def generate_prompt(doc):
    user_inputs = {
        "user_query": doc["input"],
    }
    prompt = build_prompt(**user_inputs)
    return prompt
 
# 評価
def evaluate(pred, input_text, output_text, eval_aspect):
    # プロンプトの準備
    prompt = template_prompt.format(
        input_text=input_text,
        output_text=output_text,
        eval_aspect=eval_aspect,
        pred=pred,
    )

    # 評価
    response = gemini_model.generate_content(prompt)
    num = int(response.text)
    if 1 <= num <= 5:
        return num
    raise Exception("Response Error")

# スコアの計算
def process_results(doc, results):
    score = evaluate(results[0], doc["input"], doc["output"], doc["eval_aspect"])
    return {"acc": score}