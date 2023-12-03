# Dr.KHU : 의료 상담 챗봇 🤖
## 💻 Introduction
증상을 입력하면 텍스트를 분석하여 복용할만한 약을 알려주거나, 진료 받으러 가야 할 과를 알려주는 등 의료 상담을 해주는 챗봇 제작 프로젝트 <br/>
> 💊 **증상 평가 및 처방 안내** : 간단한 증상이나 질병에 대한 기본적인 정보를 제공함으로써 사용자가 자가 진단을 할 수 있습니다. <br/>
> 🩺 **진료 및 검사 안내** : 사용자가 의료 전문가의 도움이 필요한 경우, 어떤 과를 방문해야 하는지 안내함으로써 적절한 의료 서비스를 받을 수 있습니다.<br/>
> ❗ **예방 및 건강 정보 제공** : 사용자가 건강에 대한 교육을 받으면서 예방 조치를 취함으로써 더 나은 건강 상태를 유지할 수 있습니다. <br/>
> 🚑 **응급 상황 대응** : 응급 상황에서 빠른 대처가 가능하도록 사용자에게 적절한 행동을 안내함으로써 생명을 보호할 수 있습니다. <br/>
<hr/>

## 🧑🏻‍💻 Members
| 김민아 | 류여진 | 이예원 | 최용빈 |
| :-: | :-: | :-: | :-: |
| <img src='https://avatars.githubusercontent.com/u/70475010?v=4' height=130 width=130></img> | <img src='https://avatars.githubusercontent.com/u/88676496?v=4' height=130 width=130></img> | <img src='https://avatars.githubusercontent.com/u/142980318?v=4' height=130 width=130></img> | <img src='https://avatars.githubusercontent.com/u/64704608?v=4' height=130 width=130></img> |
| <a href="https://github.com/eulneul" target="_blank"><img src="https://img.shields.io/badge/GitHub-black.svg?&style=round&logo=github"/></a> | <a href="https://github.com/ryj8075" target="_blank"><img src="https://img.shields.io/badge/GitHub-black.svg?&style=round&logo=github"/></a> | <a href="https://github.com/yewon1077" target="_blank"><img src="https://img.shields.io/badge/GitHub-black.svg?&style=round&logo=github"/></a> | <a href="https://github.com/whybe-choi" target="_blank"><img src="https://img.shields.io/badge/GitHub-black.svg?&style=round&logo=github"/></a> |


## ⚙️ Architecture
![KakaoTalk_Photo_2023-12-02-21-33-20](https://github.com/whybe-choi/khuda-nlp-project/assets/64704608/2324b7e2-048d-4017-9696-8663f4d0812e)



## 💿 Dataset
[1] [식품의약품안전처_의약품개요정보(e약은요)](https://www.data.go.kr/data/15075057/openapi.do)

[2] [건강이 궁금할 땐 하이닥](https://www.hidoc.co.kr/)


## 🔧 Model
<img width="300" alt="LangChain" src="https://github.com/whybe-choi/khuda-nlp-project/assets/88676496/d376a1b7-c9d5-41ba-be01-1efa44f3f607">
<img width="300" alt="gpt" src="https://github.com/whybe-choi/khuda-nlp-project/assets/88676496/4905e949-ada7-4290-9da8-950062ca26cd">
<img width="200" alt="Chroma" src="https://github.com/whybe-choi/khuda-nlp-project/assets/88676496/7fe464ac-e41f-4ef3-9418-6e14ebd44d54">
LangChain을 이용하여 multi-agent system을 구축하였고 이때 OpenAI api를 이용하여 모델을 사용하였다. 모델이 답변 작성 시 참고하는 데이터가 담긴 vector DB는 Chroma를 이용하였다.



## 🗣 Result
다음과 같이 챗봇 UI에 건강 관련 질문을 입력하면 진단 및 처방을 출력한다.  

<img width="742" alt="결과_질문" src="https://github.com/whybe-choi/khuda-nlp-project/assets/88676496/704c7d34-458c-4544-9713-703a14183281">
<img width="729" alt="스크린샷 2023-12-03 오후 2 48 01" src="https://github.com/whybe-choi/khuda-nlp-project/assets/64704608/8792e339-87b3-4835-800e-ec6a5c3afe51">


## 📖Reference
- [Youtube - 모두의 AI : Langchain 뿌시기](https://www.youtube.com/playlist?list=PLQIgLu3Wf-q_Ne8vv-ZXuJ4mztHJaQb_v) 
- [Medium - Corca : LLM Multi Agent: Customer Service를 기깔나게 자동화하는 방법](https://medium.com/corca/llm-multi-agent-customer-service%EB%A5%BC-%EA%B8%B0%EA%B9%94%EB%82%98%EA%B2%8C-%EC%9E%90%EB%8F%99%ED%99%94%ED%95%98%EB%8A%94-%EB%B0%A9%EB%B2%95-2eaec7654385)