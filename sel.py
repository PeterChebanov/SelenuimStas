from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get("https://www.ebay.com/")
time.sleep(5)


# Проверка карусели на прокрутку
carousel_dots_xpath = '//div[@class="vl-carousel--dots"]/ul'
active_carousel_dot_class_name_xpath = '[@class="vl-carousel--dots__active"]'
active_carousel_class_name = "vl-carousel--dots__active"


amount_of_carousel_iterations = 0
start_time = time.time()

while True:
    """
     Этот цикл while будет крутиться 45 секунд (строка 32) и вне зависимости ни от чего закончиться в это время.
     
     Основная идея в течение 45 секунд мы по очереди берем каждый элемент li, и проверяем его класс, если этот класс ==
     классу активного элемента а не null, пишем в общий счетчик amount_of_carousel_iterations +1 
     В конце цикла мы ожидаем что кол-во итераций будет больше 4, т.к. элемента всего 4.
     Таким образом мы проверим что карусель переключается + зацикленна. В моем случае кол-во итераций было 12 за 45 сек.
    """
    for i in range(1, 5):
        current_elem = WebDriverWait(driver, 15).until(EC.visibility_of_element_located(
            (By.XPATH, carousel_dots_xpath + f"/li[{i}]" + active_carousel_dot_class_name_xpath)))

        if current_elem.get_attribute('class') == active_carousel_class_name:
            amount_of_carousel_iterations += 1

    if time.time() - start_time > 45:
        break

assert amount_of_carousel_iterations > 4



#проверка кнопок

play_button_xpath = '//button[@aria-label="Play Banner Carousel"]'
pause_button_xpath = '//button[@aria-label="Pause Banner Carousel"]'
next_button_xpath = '//button[@class="carousel__control carousel__control--next" and @aria-label="Go to next banner"]'
previous_button_xpath = '//button[@class="carousel__control carousel__control--prev" and @aria-label="Go to previous banner"]'


# Проверка кнопка паузы работает
driver.refresh()  # Обновляем браузер

pause_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
            (By.XPATH, pause_button_xpath)))
pause_button.click() # Находим и нажимаем кнопку паузы карусели
time.sleep(2)


carousel_elements = driver.find_elements(By.XPATH, carousel_dots_xpath + "/li") #Собираем лист всех 4 li элементов
active_element = 0 #это будет тот элемент на котором мы остановимся после нажатия кнопки паузы (он как я заметил
# по дефолту переходит на 1ый элемент после нажатия, но мы напишем так, чтобы исполнялось даже если бы такого не было


for i, li in enumerate(carousel_elements, start=1): # здесь узнаем на каком элементе у нас произошла остановка
    class_name = li.get_attribute('class')  # тупо бежим по всем элементам и сравниваем его классы, нам нужно найти
    if class_name == active_carousel_class_name: # тот класс что не null, его название в переменной active_carousel_class_name
        active_element = i #как только нашли, записываем номер нашего li в переменную.
        break

for i in range(10): # здесь 10 раз ищем наш конкретный элемент на котором мы остановились,
    current_li_element = driver.find_element(By.XPATH, carousel_dots_xpath + f"/li[{active_element}]")
    class_of_current_element = current_li_element.get_attribute('class')
    assert class_of_current_element == active_carousel_class_name #  каждый раз проверяем что его класс это тот самый класс который для активного элемента
    time.sleep(0.7) #отдыхаем 0.7 секунд, и все заново.
# таким образом мы просто проверяем что в течение какого-то времени, после того как мы нажали книпку паузы, наш элемент не менялся, а значит не двигался


print("Если ты читаешь это сообщение, значит мы не пизданулись ни на одном assert и все работает")


driver.quit()
