# ______________________________________________________________________________________________________
# Задача 1. Доработать класс FlatIterator в коде ниже. Должен получиться итератор, который принимает
# список списков и возвращает их плоское представление, т. е. последовательность, состоящую из вложенных элементов.
# Функция test в коде ниже также должна отработать без ошибок

# Создаем класс итератора списка
class FlatIterator:

    # Передаем в __init__ список списков
    def __init__(self, list_of_lists):
        self.list_of_lists = list_of_lists

    # Создаем счетчики списков и значений
    def __iter__(self):
        self.list_counter = 0
        self.value_counter = 0
        return self

    # Предусматриваем итерацию по значениям и спискам с выходом из итератора
    # при достижении последнего значения последнего списка
    def __next__(self):
        if self.list_counter >= len(self.list_of_lists):
            raise StopIteration

        self.current_list = self.list_of_lists[self.list_counter]
        self.current_value = self.current_list[self.value_counter]

        if self.value_counter + 1 < len(self.current_list):
            self.value_counter += 1

        else:
            self.list_counter += 1
            self.value_counter = 0

        return self.current_value

# Создаем функцию - тест для определения корректности работы итератора
def test_1():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

# Запускаем тестовую функцию
if __name__ == '__main__':
    test_1()


# ______________________________________________________________________________________________________
# Задача 2. Доработать функцию flat_generator. Должен получиться генератор, который принимает список списков
# и возвращает их плоское представление.Функция test в коде ниже также должна отработать без ошибок.

import types

# Создаем функцию, проходящую по каждому значению каждого списка, вложенного в список списков
def flat_generator(list_of_lists):
    for item in list_of_lists:
        for value in item:
            yield value

# Создаем функцию - тест для определения корректности работы итератора
def test_2():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)

# Запускаем тестовую функцию
if __name__ == '__main__':
    test_2()


# ______________________________________________________________________________________________________
# Задача 3.* Необязательное задание. Написать итератор, аналогичный итератору из задания 1,
# но обрабатывающий списки с любым уровнем вложенности.

# Создаем класс расширенного итератора списков
class FlatIterator2:
    # Используем стек итераторов
    def __init__(self, list_):
        self._stack = [iter(list_)]

    def __iter__(self):
        return self

    def __next__(self):

        while self._stack:
            # Итерируемся по стеку
            try:
                # Если следующего значение в списке нет, останавливаем итерацию
                item = next(self._stack[-1])
            except StopIteration:
                # Извлекаем элемент из стека, уменьшая его на этот элемент
                self._stack.pop()
                continue
            # Делаем проверку на вложенный список
            if not isinstance(item, list):
                return item
            # Если проверка пройдена - итерируем вложенный список в стеке
            self._stack.append(iter(item))
        raise StopIteration

# Создаем функцию проверки работы итератора
def test_3():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator2(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator2(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']

# Запускаем проверку
if __name__ == '__main__':
    test_3()


# ______________________________________________________________________________________________________
# Задача 4. *Необязательное задание. Написать генератор, аналогичный генератору из задания 2,
# но обрабатывающий списки с любым уровнем вложенности.

# Создаем функцию
def flat_generator2(list_of_lists):
    """Генератор позволяет  возвращать эелементы из списка списков с любым уровнем вложености"""
    for elem in list_of_lists:
        # Проверяем, является ли списком следующий элемент
        if isinstance(elem, list):
            # если следующий элемент - список, снова вызываем эту функцию
            for sub_elem in flat_generator2(elem):
                yield sub_elem
        # если следующий элемент не список, то возвращаем этот элемент
        else:
            yield elem

# Создаем функцию проверки работы генератора
def test_4():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator2(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):

        assert flat_iterator_item == check_item

    assert list(flat_generator2(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']

    assert isinstance(flat_generator2(list_of_lists_2), types.GeneratorType)

# Запускаем проверку
if __name__ == '__main__':
    test_4()
