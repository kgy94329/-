'''
AI실무 개발 14주차 과제
작성자: 권구영
학 번: 202330852
내 용:
14주차 실습 자료를 참고하여,
기존 TF-IDF와 Consine Similarlity를 이용해 챗봇을 구현한 코드를
레벤슈타인 거리를 기반으로 한 챗봇으로 수정하여 구현하시오.
'''
import pandas as pd

# 챗봇 클래스를 정의
class SimpleChatBot:
    # 챗봇 객체를 초기화하는 메서드, 초기화 시에는 입력된 데이터 파일을 로드하고 질문과 답변을 각 변수에 저장.
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)

    # CSV 파일로부터 질문과 답변 데이터를 불러오는 메서드
    def load_data(self, filepath):
        data = pd.read_csv(filepath) # 데이터 파일인 csv파일을 연다.
        questions = data['Q'].tolist()
        answers = data['A'].tolist()
        return questions, answers

    # 답변을 생성하는 메서드
    def get_response(self, user_question):
        min_dist = float('inf') # 크기가 가장 큰 float값을 선언하고, 최소 거리를 찾는 지표로 활용한다.
        best_idx = -1 # 최소거리 일 때의 답변을 반환하기 위해 인덱스를 저장

        for i, data in enumerate(self.questions): # 모든 질문 데이터를 조회하고 최적의 답을 찾는다.
            distance = self.levenshtein_dist(user_question, data)
            if distance < min_dist:
                min_dist = distance
                best_idx = i

        return self.answers[best_idx]
    
    # 레벤슈타인 거리를 구하는 메서드
    # 레벤슈타인 거리 알고리즘은 두 비교군의 삽입, 교체, 삭제에 대한 비용을 계산하고
    # 연산되는 비용이 클 수록 다른 것으로 본다.
    def levenshtein_dist(self, s1, s2):
        if len(s1) < len(s2): # s1을 항상 더 길거나 같게 유지
            return self.levenshtein_dist(s2, s1)

        if len(s2) == 0: # s2가 빈 문자열이면, s1의 길이가 편집 거리
            return len(s1)

        pre_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insert = pre_row[j + 1] + 1 # 삽입
                delet = current_row[j] + 1 # 삭제
                replace = pre_row[j] + (c1 != c2) # 교체
                current_row.append(min(insert, delet, replace)) # 최소값을 현재 행에 저장
            pre_row = current_row
        
        return pre_row[-1]

# 데이터 파일의 경로를 지정.
filepath = './data/ChatbotData.csv'

# 챗봇 객체를 생성.
chatbot = SimpleChatBot(filepath)

# '종료'라는 입력이 나올 때까지 사용자의 입력에 따라 챗봇의 응답을 출력하는 무한 루프를 실행.
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        break
    response = chatbot.get_response(input_sentence)
    print('Chatbot:', response)
