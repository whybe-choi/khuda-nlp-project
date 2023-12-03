#데이터 크롤링

from selenium import webdriver 
from selenium.webdriver import ActionChains 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote_plus
import time
import sys
import pandas as pd
import os
import multiprocessing


dataset = pd.DataFrame(columns = ['question', 'answer', 'department'])
csv_list = ['가정의학과', '소화기내과', '신경과', '산부인과', '재활의학과', '비뇨의학과', '이비인후과', '정신건강의학과',
            '정형외과', '피부과']
url_code =['PF000', 'PMG00', 'PN000', 'PY000', 'PR000', 'PU000', 'PE000', 'PP000',
          'PO000' ,'PS000']


def do_multi(code):
    for departments in range(len(csv_list)):
        os.mkdir("{}".format(csv_list[departments]))
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        dr = webdriver.Chrome(options=options)
        act = ActionChains(dr)
        html = dr.page_source
        soup = BeautifulSoup(html, "html.parser")
        time.sleep(2)
        
        if code == '1':
            start, end = 1,91
        elif code == '2':
            start, end = 91, 181 
        elif code == '3':
            start, end = 181, 271
        else:
            start, end = 271,361

        try:
            for pagenum in range(start, end):
                url = "https://www.hidoc.co.kr/healthqna/part/list?code={}&page=".format(url_code[departments]) + str(pagenum) 
                dr.get(url)
                time.sleep(0.5)
                for postnum in range(4, 11):
                    element2 = dr.find_element('xpath', '//*[@id="hidocBody"]/div[1]/div[{}]/div[1]/div/a'.format(postnum))  
                    act.click(element2).perform()

                    patient = dr.find_element(By.CSS_SELECTOR, '#hidocBody > div.health_view > div.box_type1.view_question > div.inner > div.desc > p').text
                    doctor = dr.find_element(By.CSS_SELECTOR, '#hidocBody > div.health_view > div.view_answer > div:nth-child(29) > div.answer_body > div > div:nth-child(1)').text
                        
                    replace_list = ['<br/>', '<p>', '</p>', '<div class="desc">','</div>']
                    for i in replace_list:
                        patient = patient.replace(i, '')
                        doctor = doctor.replace(i, '')
                    dataset.loc[len(dataset)] = [patient, doctor, csv_list[departments]]
                    dr.back()
        except:
            print('The end')
        dataset.to_csv('{}/dataset{}.csv'.format(csv_list[departments],code), encoding='utf-8-sig')
    
def main():
    
    code_list = ['1','2','3','4']

    pool = multiprocessing.Pool(4)


    pool.map(do_multi, code_list)


    pool.close()
    pool.join()


#데이터 전처리


def concat_parts(csv_list):
    for i in csv_list:
        folders = os.listdir(f'{i}')
        df_all = pd.DataFrame(columns = ['question', 'answer', 'department'])
        for files in folders:
            dir = i + '/'+ files
            df = pd.read_csv(dir, encoding = 'utf-8', index_col = 0)
            df_all = pd.concat([df_all, df])

        df_all.reset_index(drop=True, inplace=True)
        idx = df_all[df_all['answer'].str.contains('질문자의 감사 인사')].index
        df_drop = df_all.drop(index = idx)


        idx2 = df_drop[df_drop['question'].str.contains('질문자 본인의 요청')].index
        df_drop = df_drop.drop(index = idx2)
        df_drop.to_csv('{}.csv'.format(i), encoding = 'utf-8-sig')

def concat_all(csv_list):
    df_result = pd.DataFrame(columns=['question', 'answer', 'department'])
    for i in csv_list:
        df = pd.read_csv(f'{i}.csv', encoding = 'utf-8', index_col = 0)
        df_result = pd.concat([df_result,df])
    df_result.reset_index(drop=True, inplace=True)
    df_result.columns = ["question", "answer", "department"]
    df_result.to_csv('df_all.csv', encoding = 'utf-8-sig')



import numpy as np



def prepro(df):
#한글, 공백, 숫자 제외 모두 제거
    df['question'] = df['question'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣0-9 ]", "")
    df['question'].replace('', np.nan, inplace=True)

    df['answer'] = df['answer'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣0-9 ]", "")
    df['answer'].replace('', np.nan, inplace=True)


    # 특정 문자열 "안녕하세요"만 제거
    df['question'] = df['question'].str.replace("안녕하세요", "")
    df['question'] = df['question'].str.replace(" +", " ")
    df['answer'] = df['answer'].str.replace("안녕하세요", "")
    df['answer'] = df['answer'].str.replace(" +", " ")

    # "안녕하세요. 하이닥 ~ 상담의" 다음에 오는 부분을 지우기
    df['answer'] = df['answer'].str.replace("하이닥", "")
    df['answer'] = df['answer'].str.replace(" +", " ")

    # "과 상담의 ~입니다." 부분을 정규표현식으로 지우기
    df['answer'] = df['answer'].str.replace(r'(.*)과 상담의 (.*)입니다.', '', regex=True)
    df['answer'] = df['answer'].str.replace(" +", " ")

    df['question'] = df['question'].str.replace('\n', '')
    df['answer'] = df['answer'].str.replace('\n', '')
    df['answer'] = df['answer'] + ' ' + df['department'] + '로 가세요.'


    df.to_csv('df_final.csv', encoding = 'utf-8-sig')

if __name__ == '__main__':
    
    main()
    concat_parts(csv_list)
    concat_all(csv_list)
    df = pd.read_csv('df_all.csv', encoding='utf-8', index_col=0)
    prepro(df)