import undetected_chromedriver as uc
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import sched
import time


def get_table_orders(drv):
    try:
        table_orders = drv.find_element(By.XPATH,
                                       '/html/body/div[1]/div/div[1]/div/div/div[3]/div[4]/div[1]/div[1]/div/div[2]')
        return table_orders.find_elements(By.CLASS_NAME, 'b9f')
    except NoSuchElementException:
        print("Ошибка при поиске элементов")
        return None


def get_orders_dict(drv):
    table = get_table_orders(drv)
    if table:
        for i in range(len(table)):
            print(f"{i+1}.", end="")
            print(table[i].find_element(By.CLASS_NAME, 'tsBodyM').find_element(By.TAG_NAME, 'span').text)


def add_order(drv):
    try:
        add_button = drv.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div[3]/div[3]/div[3]/div/div[19]/div[1]/div/div/div/div[1]/button')
        add_button.click()
    except NoSuchElementException:
        print("Ошибка при добавлении продукта в корзину")
        return None


def buy_orders(price_max: int, drv):
    #drv.get('https://www.ozon.ru/cart')

    try:
        price_el = drv.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div/div[3]/div[4]/div[2]/div/section/div[1]/div[2]/div[4]/span[2]')
        price = ''.join(ch for ch in price_el.text if ch.isalnum())
        if int(price) < price_max:
            pre_offer_button = drv.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div/div[3]/div[4]/div[2]/div/section/div[1]/div[1]/div[1]/button')

            pre_offer_button.click()
    except NoSuchElementException:
        print("Ошибка при оформлениии")
        return None

    try:
        drv.implicitly_wait(2)
        price_el = drv.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div[4]/div/div/div[2]/div[3]/div/section/div[1]/div[2]/div[5]/span[2]')
        print(f"price_el.text : {price_el.text}")
        price = ''.join(ch for ch in price_el.text if ch.isalnum())
        if int(price) < price_max:
            offer_button = drv.find_element(By.XPATH,
                                                '/html/body/div[1]/div/div[1]/div[4]/div/div/div[2]/div[3]/div/section/div[1]/div[1]/div[1]/button')
            #offer_button.click()
            print(f"Условие выполнено: {price}")
    except NoSuchElementException:
        print("Ошибка: при заказе товара")
        return None


def set_timer(drv):
    while True:
        price = input("Укажите цену товара товара: \n")
        if price.isalnum():
            break
        else:
            print("Ошбика: цена указано неправильно")

    while True:
        date_str = input("Введите дату и вермя в формате %d/%m/%Y %H:%M:%S:\n")
        try:
            date = time.strptime(date_str, "%d/%m/%Y %H:%M:%S")
            break
        except ValueError:
            print("Ошибка: неправильно заданы дата и время")

    delta = time.mktime(date) - time.mktime(time.localtime())
    s = sched.scheduler()
    s.enter(delta, 1, buy_orders, [price, drv])
    s.run()


if __name__ == '__main__':
    options = uc.ChromeOptions()
    options.add_argument('--user-data-dir=C:\\Users\\Admin\\AppData\\Local\\Google\\Chrome\\User Data')
    options.add_argument(r'--profile-directory=Default')
    driver = uc.Chrome(options=options)
    driver.get('https://www.ozon.ru/cart')
    # get_orders_dict(driver)
    # buy_orders(1000, driver)
    set_timer(driver)

    input("Скрипт отработан \n Нажмите любую клавишу... \n")
    driver.quit()
