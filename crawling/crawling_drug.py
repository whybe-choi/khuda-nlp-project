import aiohttp
import asyncio
import os
from dotenv import load_dotenv
import csv

async def fetch(session, url, params, csv_writer):
    async with session.get(url, params=params) as response:
        try:
            result = await response.json()
            items = result["body"]["items"]
            for item in items:
                entpName =  item["entpName"]
                itemName = item["itemName"]
                itemSeq = item["itemSeq"]
                efcyQesitm = item["efcyQesitm"]
                useMethodQesitm = item["useMethodQesitm"]
                atpnWarnQesitm = item["atpnWarnQesitm"]
                atpnQesitm = item["atpnQesitm"]
                intrcQesitm = item["intrcQesitm"]
                seQesit = item["seQesitm"]
                depositMethodQesitm = item["depositMethodQesitm"]
                openDe = item["openDe"]

                csv_writer.writerow([entpName, itemName, itemSeq, efcyQesitm, useMethodQesitm,
                                    atpnWarnQesitm, atpnQesitm, intrcQesitm, seQesit, depositMethodQesitm,
                                    openDe])
        except:
            pass

async def main():
    load_dotenv()
    serviceKey = os.getenv('SERVICE_KEY')

    BASE_URL = 'http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList'
    urls = [f"{BASE_URL}?pageNo={i}" for i in range(1, 400)]

    params ={'serviceKey' : serviceKey, 
         'numOfRows' : '10', 
         'entpName' : '', 
         'itemName' : '',
         'itemSeq' : '', 
         'efcyQesitm' : '', 
         'useMethodQesitm' : '', 
         'atpnWarnQesitm' : '', 
         'atpnQesitm' : '', 
         'intrcQesitm' : '', 
         'seQesitm' : '', 
         'depositMethodQesitm' : '', 
         'openDe' : '', 
         'updateDe' : '', 
         'type' : 'json' }
    
    # try:
    #     os.mkdir("./data")
    # except:
    #     pass

    with open('../database/dataset/drug/drug_list.csv', 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['entpName', 'itemName', 'itemSeq', 'efcyQesitm', 'useMethodQesitm', 
                             'atpnWarnQesitm', 'atpnQesitm', 'intrcQesitm', 'seQesit', 'depositMethodQesitm',
                             'openDe'])

        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[fetch(session, url, params,csv_writer) for url in urls])

if __name__ == '__main__':
    asyncio.run(main())