from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from data.config import *
from utils.db_api.sqlite import *
from loader import bot
import asyncio
from utils import send_all_admin

headers={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.116 YaBrowser/22.1.1.1544 Yowser/2.5 Safari/537.36'
}
user_agent= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.116 YaBrowser/22.1.1.1544 Yowser/2.5 Safari/537.36'
def get_page(suma, curr):
    try:
        n=99
        if curr=="BTC":
            n=2
            url= f'https://blockchair.com/bitcoin/address/{wallet_btc}'

        elif curr=="LTC":
            n=4
            url= f'https://blockchair.com/litecoin/address/{wallet_ltc}'

        elif curr=="ETH":
            url= f'https://blockchair.com/ethereum/address/{wallet_eth}'

        elif curr=="BNB1":
            url= f'https://blockchair.com/bnb/address/{wallet_BNB1}'

        elif curr=="USDT1": # не ворк
            url= f'https://blockchair.com/ethereum/address/{wallet_usdt1}'

        elif curr=="USDT2": 
            url= f'https://blockchair.com/bnb/address/{wallet_usdt2}'

        elif curr=="BNB2": # не ворк
            url= f'https://blockchair.com/ethereum/address/{wallet_BNB2}' # пока не создано

        elif curr=="USDT3": 
            url= f'https://tronscan.org/#/address/{wallet_usdt3}/transfers' # пока не создано

        if curr=="BTC" or curr=="LTC" or curr=="ETH":
            options = Options()
            options.add_argument("--headless")
            options.add_argument(f'user-agent={user_agent}')
            options.add_argument('--log-level=3')
            options.add_argument("--ignore-certificate-error")
            options.add_argument("--ignore-ssl-errors")
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
            driver.get(url)
            time.sleep(5)
            xpath='//*[@id="address-transactions"]/div[1]/div/div[1]/div[3]/span/span/span[1]'
            price=driver.find_elements('xpath',xpath)
            xpath2='//*[@id="address-transactions"]/div[1]/div/div[1]/div[2]'
            conf=driver.find_elements('xpath',xpath2)
            for i in range(len(price)):
                if price[i].text==suma and ('Confirmed' == conf[i].text or int(conf[i].text[13:15]) >= n):
                    driver.quit()
                    return True
            driver.quit() 
            return False
        if curr == "BNB1" or curr=="USDT2":
            options = Options()
            options.add_argument("--headless")
            options.add_argument(f'user-agent={user_agent}')
            options.add_argument('--log-level=3')
            options.add_argument("--ignore-certificate-error")
            options.add_argument("--ignore-ssl-errors")
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
            driver.get(url)
            time.sleep(1)
            xpath='//*[@id="app"]/div[2]/div/div/div[5]/div[2]/div[1]/div/div/div/table/tbody/tr/td[3]/span[1]/span[1]/span'
            price=driver.find_elements('xpath',xpath)
            xpath2='//*[@id="app"]/div[2]/div/div/div[5]/div[2]/div[1]/div/div/div/table/tbody/tr/td[4]/span/span[1]/span'
            conf=driver.find_elements('xpath',xpath2)
            for i in range(len(price)):
                if price[i].text[1:]==suma and conf[i].text=='Yes':
                    driver.quit()
                    return True
            driver.quit()
            return False
        if curr == "USDT3":
            options = Options()
            options.add_argument("--headless")
            options.add_argument(f'user-agent={user_agent}')
            options.add_argument('--log-level=3')
            options.add_argument("--ignore-certificate-error")
            options.add_argument("--ignore-ssl-errors")
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
            driver.get(url)
            time.sleep(4)
            xpath='//*[@id="popupContainer"]/div[2]/div/div/div/div/div/div/div/table/tbody/tr/td[2]/div/div/span'
            price=driver.find_elements('xpath',xpath)
            xpath2='//*[@id="popupContainer"]/div[2]/div/div/div/div/div/div/div/table/tbody/tr/td[4]/div/span/span/span/span'
            conf=driver.find_elements('xpath',xpath2)
            for i in range(len(price)):
                if price[i].text[0]=='+' and price[i].text[1:]==suma and conf[i].text=='CONFIRMED':
                    driver.quit()
                    return True
            driver.quit()
            return False
    except Exception as e:
        print(e)


async def pushup():
    while True:
        await asyncio.sleep(300)
        today = datetime.datetime.now()
        datas = get_check()
        for data in datas:
            difference = (today) - (datetime.datetime.strptime(data[4], "%d-%H-%M"))
            hours = divmod(difference.seconds, 3600)[0]
            if hours<5:
                if get_page(data[1],data[3]):
                    print(f'Покупка прошла успешно {data[3]}')
                    get_user_info = get_userx(user_id=data[0])
                    update_userx(data[0],
                    balance=str(round(float(get_user_info[4]) + float(data[2]),2)))
                    remove_check(data[0])
                    await bot.send_message(chat_id=data[0],text=f"<b>✅ You have successfully topped up your balance in the amount of {data[2]}$. Good luck ❤</b>\n")
                    await send_all_admin(f"<b>💰 User</b> "
                                            f"(@{get_user_info[2]}|<a href='tg://user?id={data[0]}'>{get_user_info[3]}</a>"
                                            f"|<code>{data[0]}</code>) "
                                            f"<b>replenished the balance by the amount of</b> <code>{data[2]}$</code> 🥝\n")
                else:
                    print(f'Покупка не нашлась {data[3]}')
            else:
                remove_check(data[0])
        