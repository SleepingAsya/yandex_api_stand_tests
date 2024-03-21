import sender_stand_request
import data


# Доп.функция для получения актуального токена пользователя
def get_auth_token():
    token = sender_stand_request.post_new_user(data.user_body).json()["authToken"]
    return token

# Функция для изменения значения у ключа name в теле запроса:
# Копируем словарь с телом запроса из файла data
# Изменяем значение для ключа name
# Возвращаем новый словарь с нужным значением name
def get_kit_body_with_new_name(new_name):
    current_body = data.kit_body.copy()
    current_body["name"] = new_name
    return current_body

# Функция для позитивной проверки создания набора:
# new_kit_body - сохраняем обновлённое тело запроса
# kit_response - сохраняем результат запроса на создание набора
# Проверяем, что код ответа равен 201
# Проверяем, что в ответе name такое же, как в запросе
def positive_assert(name):
    token = get_auth_token()
    new_kit_body = get_kit_body_with_new_name(name)
    kit_response = sender_stand_request.post_new_kit(new_kit_body, token)
    assert kit_response.status_code == 201
    assert kit_response.json()["name"] == new_kit_body["name"]
    print(kit_response.json())

# Функция негативной проверки, когда в ответе ошибка связанная с символами:
# new_kit_body - сохраняем обновлённое тело запрос
# kit_response - сохраняем результат
# Проверяем, что код ответа равен 400
def negative_assert_code_400(name):
    token = get_auth_token()
    new_kit_body = get_kit_body_with_new_name(name)
    kit_response = sender_stand_request.post_new_kit(new_kit_body, token)
    assert kit_response.status_code == 400
    print(kit_response.json())

# Тест 1. Успешное создание набора. Параметр name состоит из 511 символов
def test_create_kit_1_letter_in_name_get_success_response():
    positive_assert("а")

# Тест 2. Успешное создание набора. Параметр name состоит из 1 символа
def test_create_kit_511_letter_in_name_get_success_response():
    positive_assert("Abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd\
    abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd\
    abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcd\
    abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd\
    abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd\
    abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabC")

# Тест 3. Ошибка. Параметр name состоит из 0 символов
def test_create_kit_0_letter_in_name_get_error_response():
    negative_assert_code_400("")

# Тест 4. Ошибка. Параметр name состоит из 512 символов
def test_create_kit_512_letter_in_name_get_error_response():
    negative_assert_code_400("Abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd\
    abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdab\
    cdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcd\
    abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd\
    abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd\
    abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcD")

# Тест 5. Успешное создание набора. Параметр name состоит из английских символов
def test_create_kit_english_letter_in_name_get_success_response():
    positive_assert("QWErty")

# Тест 6. Успешное создание набора. Параметр name состоит из русских символов
def test_create_kit_russian_letter_in_name_get_success_response():
    positive_assert("Мария")

# Тест 7. Успешное создание набора. Параметр name состоит из спец.символов
def test_create_kit_has_special_symbol_in_name_get_success_response():
    positive_assert("№%@,")

# Тест 8. Успешное создание набора. Параметр name сожержит пробел
def test_create_kit_has_space_in_name_get_success_response():
    positive_assert("Человек и Ко")

# Тест 9. Успешное создание набора. Параметр name состоит из цифр
def test_create_has_with_number_in_name_get_success_response():
    positive_assert("123")

# Написала доп.функцию для работы теста 10 с отсутсвием параметра
def negative_assert_no_name(name):
    token = get_auth_token()
    kit_response = sender_stand_request.post_new_kit(name, token)
    assert kit_response.status_code == 400
    print(kit_response.json())

# Тест 10. Ошибка. В запросе не передан параметр name
# Копируем словарь с телом запроса из файла data в переменную kit_body
# Удаляем параметра name из запроса
# Проверяем полученный ответ
def test_create_user_no_name_get_error_response():
    kit_body = data.kit_body.copy()
    kit_body.pop("name")
    negative_assert_no_name(kit_body)

# Тест 11. Ошибка. Тип параметра name - число:
# new_kit_body сохраняем обновлённое тело запроса
# kit_response сохраняем результат запроса на создание пользователя
# Проверяем код ответа
def test_create_user_number_type_name_get_error_response():
    token = get_auth_token()
    new_kit_body = get_kit_body_with_new_name(123)
    kit_response = sender_stand_request.post_new_kit(new_kit_body, token)
    assert kit_response.status_code == 400
    print(kit_response.json())