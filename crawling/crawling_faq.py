import json
import time
from playwright.sync_api import sync_playwright

def extract_title(page):
    try:
        title_content = page.query_selector('strong.tit').inner_text()
        return title_content
    except Exception as e:
        print(f"Failed to retrieve title content for {page.url}: {e}")
        return None

def extract_smart_tags(page):
    try:
        smart_tag_elements = page.query_selector_all('span.tag_desc')
        smart_tags = [element.inner_text().strip() for element in smart_tag_elements]
        return smart_tags
    except Exception as e:
        print(f"Failed to retrieve smart tags for {page.url}: {e}")
        return None

def extract_question(page):
    try:
        question_content = page.query_selector('div.desc').inner_text()
        return ' '.join(question_content.split())
    except Exception as e:
        print(f"Failed to retrieve question content for {page.url}: {e}")
        return None

def extract_answers(page):
    try:
        answer_elements = page.query_selector_all('div.answer_body > div.cont > div.desc')
        answer_texts = [' '.join(element.inner_text().split()) for element in answer_elements]
        return ' '.join(answer_texts)
    except Exception as e:
        print(f"Failed to retrieve answer contents for {page.url}: {e}")
        return None

def extract_info_from_page(page, href):
    page.goto(href)
    page.wait_for_load_state('load')

    info = {
        "link": page.url,
        "title": extract_title(page),
        "smart_tags": extract_smart_tags(page),
        "question": extract_question(page),
        "answer": extract_answers(page)
    }

    print(json.dumps(info, ensure_ascii=False, indent=4))

    return info

def run(playwright):
    start_time = time.time()
    faq_list = []
    
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    
    base_url = "https://hidoc.co.kr/healthqna/faq/list?orderType=15010&page="

    for page_number in range(1, 1022):
        page.goto(base_url + str(page_number))
        page.wait_for_load_state('load')
        
        a_elements = page.query_selector_all('strong.tit_qna a')
        hrefs = [element.get_attribute('href') for element in a_elements]
        
        for href in hrefs:
            if href:
                if not href.startswith('http'):
                    href = f"https://hidoc.co.kr{href}"
                info = extract_info_from_page(page, href)
                faq_list.append(info)
    
    browser.close()

    # JSONL 파일로 저장
    with open('datasets/faq_list.jsonl', 'w', encoding='utf-8') as f:
        for item in faq_list:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")

with sync_playwright() as playwright:
    run(playwright)
