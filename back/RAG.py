from sentence_transformers import SentenceTransformer, util
import numpy as np
import pandas as pd
from openai import OpenAI

class Rag:
    def __init__(self):
        # 별도 가이드 파일을 딕셔너리화 한 것
        company_names = [
            {"eng": "katalk(1)", "kor": "카톡"},
            {"eng": "katalk(2)", "kor": "카톡"},
            {"eng": "baemin", "kor": "배민"},
            {"eng": "guppi", "kor": "구삐"},
        ]
        # 객체의 guide 값은 company_names를 속성으로 갖는 read_guide 함수 값이다.
        self.guide = self.read_guide(company_names)
        # 객체의 embedder 값은 SentenceTransformer("BM-K/KoSimCSE-roberta-multitask") 로 한다.
        self.embedder = SentenceTransformer("BM-K/KoSimCSE-roberta-multitask")
        # 객체의 embed_guide 값은 guide_embedding 함수의 return 값이 된다.
        self.embed_guide = self.guide_embedding()

    # guide_file 폴더에 있는 가이드들을 태그 달아서 하나의 리스트로 가져옴
    def read_guide(self, file_list):
        all_guides = []

        for file in file_list:
            path = f"/Users/parkjiyoung/Desktop/computer_study/project/fin_dap/back/guide_file/{file['eng']}.txt"

            with open(path, 'r', encoding='utf-8') as file_content:
                guides = file_content.read().split("\n\n^^\n\n")
            last_guide = [f"[{file['kor']}] " + guide for guide in guides]

            all_guides += last_guide

        return all_guides

    def guide_embedding(self):
        corpus_embedding = self.embedder.encode(
            self.guide, convert_to_tensor=True)
        return corpus_embedding

    def make_prompt(self, query, k):
        top_k = k
        cnt = 1

        prompt = []

        # quide와 똑같이 query 인코딩
        query_embedding = self.embedder.encode(query, convert_to_tensor=True)
        # cosine 비교
        cos_scores = util.pytorch_cos_sim(query_embedding, self.embed_guide)[0]
        cos_scores = cos_scores.cpu()
        # np.argpartition을 사용하여 상위 k 개의 인덱스 추출
        top_results = np.argpartition(-cos_scores, range(top_k))[:top_k]
        idxs = [x.item() for x in top_results]

        prompt.append("아래 정보들을 참고해서 질문에 대한 답을 알려줘. 정보 부분의 숫자는 질문과 얼마나 유사한지를 나타내는 지표고, 대괄호 안의 단어는 어플 이름이야. 꼭 질문과 관련 없는 어플 이름은 사용하지 말고, 질문에 대해 필요한 정보만 사용해. 질문과 관련이 있는 질문에 대한 답변만 알려 주고, 질문에 대한 적절한 답이 없다면 답변이 불가하다고 알려줘.")
        prompt.append(f"### 질문 ###")
        prompt.append(query)

        # 점수 계산
        scores = []
        for idx in idxs:
            score = float("%.2f" % cos_scores[idx])
            scores.append(score)
            if scores[0] >= 0.5:
                prompt.append(f"### 정보{cnt} ###")
                prompt.append("%.2f" % cos_scores[idx])
                prompt.append(self.guide[idx].strip())
            else:
                prompt.append("### 정보 ###")
                prompt.append("적절한 답이 없습니다.")
                break

            cnt += 1

        scores = []
        cnt = 1
        prompt = '\n'.join(prompt)
        # print(prompt)
        return prompt

    def gpt_api(self, query, k):
        with open("/Users/parkjiyoung/Desktop/computer_study/project/pass_key/gpt_api.txt", "r") as key:
            pass_key = key.read()
        client = OpenAI(
            api_key = pass_key,
            )

        prompt = self.make_prompt(query, k)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        reply = response.choices[0].message.content.strip()
        print(reply)
        return reply
