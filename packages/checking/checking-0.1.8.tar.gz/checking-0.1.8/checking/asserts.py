from contextlib import contextmanager
from typing import Any, Type

from .exceptions import ExceptionWrapper
from .exceptions import TestBrokenException
from .classes.basic_listener import short


def is_true(obj: Any, message: str = None):
    """
    Проверка объекта на истинность (truthy)
    :param object: любой объект для проверки
    :return: None
    """
    if not obj:
        _message = _mess(message)
        raise AssertionError(f'{_message}Expected True, but got False! ')


def is_false(obj: Any, message: str = None):
    """
    Проверка объекта на не истинность (falsy)
    :param obj: любой объект для проверки
    :return: None
    """
    if obj:
        _message = _mess(message)
        raise AssertionError(f'{_message}Expected False, but got True')


def equals(expected: Any, actual: Any, message: str = None):
    """
    Сравнивает равенство двух объектов
    :param expected: ожидаемый объект
    :param actual: актуальный объект
    :param message: сообщение, которое будет указано при провале проверки
    :return: None
    :raises AssertionError если объекты не равны, с указанием объектов и их типов
    """
    if (expected is actual) or expected == actual:
        return
    _message = _mess(message)
    raise AssertionError(f'{_message}Expected "{short(expected)}" <{type(expected).__name__}>, '
                         f'but got "{short(actual)}"<{type(actual).__name__}>!')


def not_equals(expected: Any, actual: Any, message: str = None):
    """
    Проверяет, что объекты не равны
    :param expected: ожидаемый объект
    :param actual: актуальный объект
    :param message: сообщение, которое будет указано при провале проверки
    :return: None
    :raises AssertionError если объекты равны
    """
    if (expected is actual) or expected == actual:
        _message = _mess(message)
        raise AssertionError(f'Objects are equal ({short(expected)}, {short(actual)})!')


def is_none(obj: Any, message: str = None):
    """
    Проверяется, что объект является None, обратная функция для проверки not_none
    :param obj: проверяемый объект
    :param message: сообщение, которое будет указано при провале проверки
    :return: None
    :raises AssertionError с указанием типа объекта
    """
    _message = _mess(message)
    if obj is not None:
        raise AssertionError(f'{_message}Object {short(obj)}<{type(obj).__name__}> is not None!')


def not_none(obj: Any, message: str = None):
    """
    Проверяется, что объект не None, обратная функция для is_none
    :param obj: проверяемый объект
    :param message: сообщение, которое будет указано при провале проверки
    :return: None
    :raises AssertionError
    """
    _message = _mess(message)
    if obj is None:
        raise AssertionError(f'{_message}Unexpected None!')


@contextmanager
def waiting_exception(exception: Type[Exception]):
    """
    Менеджер контекста для проверки падения исключения при определенных действиях. Пример:

    with waiting_exception(ZeroDivisionError) as exc:
        some_action()
    print(exc.message) # Выведет сообщение из исключения

    :param exception: ожидаемый тип исключения, нельзя использовать BaseException, не рекомендуется использовать
    Exception (лучше использовать конкретное исключение)
    :return: контекст ExceptionWrapper, который изначально пуст, а при падении исключения получает его в параметр value
    :raises TestBrokenException если использовано BaseException или не наследники Exception
    :raises AssertionError если упало не то исключение, которое ожидалось
    :raises ExceptionWrapper если не упало исключений
    """
    fake = ExceptionWrapper()
    try:
        if exception is BaseException:
            raise TestBrokenException('You must use concrete exception, except of BaseException!')
        if not issubclass(type(exception), type(Exception)):
            raise TestBrokenException(f'Exception or its subclasses expected, but got '
                                      f'"{exception}"<{type(exception).__name__}>')
        yield fake
    except TestBrokenException as e:
        raise e
    except exception as e:
        fake.set_value(e)
        return
    except Exception as e:
        raise AssertionError(f'Expect {exception}, but raised {type(e).__name__} ("{e}")')
    else:
        raise fake


@contextmanager
def no_exception_expected():
    """
    Менеджер контекста для ситуаций, когда не ожидается падения исключений, более явно, чем просто писать тест
    без ассерта. Пример:

    with no_exception_expected():
        some_action()

    :return: None
    :raises AssertionError если исключение (любой наследник Exception) все же падает
    """
    try:
        yield
    except Exception as e:
        raise AssertionError(f'Expect no exception, but raised {type(e).__name__} ("{e}")')


@contextmanager
def mock_builtins(function_name: str, func):
    """
    EXPERIMENTAL!
    Мок встроенных функций, таких как print, input и так далее. После выхода из менеджера контекста, оригинальная
    функция снова обретает прежнее поведение.
    :param function_name: имя одной из встроенных функций python
    :param func: функция замена, которая будет вызвана вместо оригинальной
    :return:
    """
    import builtins as b
    if not hasattr(b, function_name):
        raise TestBrokenException(f'No build-in function "{function_name}"!')
    try:
        temp_ = getattr(b, function_name)
        setattr(b, function_name, func)
        yield
    finally:
        setattr(b, function_name, temp_)


@contextmanager
def mock(module_: Any, function_name: str, func: Any):
    """
    EXPERIMENTAL!
    Менеджер контекста для мокирования(подмены) любой функции или атрибута модуля
    :param module_: объект модуля (не название! он должен быть импортирован в тесте)
    :param function_name: название функции
    :param func: функция-замена, но может быть и атрибут
    :return:
    """
    if str(type(module_)) != "<class 'module'>":
        raise TestBrokenException(f'"{module_} is not a module!')
    if not hasattr(module_, function_name):
        raise TestBrokenException(f'No function "{function_name} at module {module_}"!')
    try:
        temp_ = getattr(module_, function_name)
        setattr(module_, function_name, func)
        yield
    finally:
        setattr(module_, function_name, temp_)


def test_fail(message: str = None):
    """
    Принудительный провал теста, может быть использовано в редких условиях вместо проверки заведомо неверных условий
    :param message: опциональное сообщение
    :return: None
    """
    raise AssertionError(message if message else 'Test was forcibly failed!')


def test_brake(message: str = None):
    """
    Принудительно приводим тест в сломанное состояние, может быть использовано в редких условиях вместо
    бросания исключений
    :param message: опциональное сообщение
    :return: None
    """
    raise TestBrokenException(message if message else 'Test was forcibly broken!')


def contains(part: Any, whole: Any, message: str = None):
    """
    Проверяется, что один объект является частью (входит) второго. Аналогично проверке a in b
    :param part: объект-часть, который входит в целое
    :param whole: объект-целое, которое содержит часть
    :param message: опциональное сообщение
    :return: None
    :raises AssertionError если один объект не является частью второго
    :raises TestBrokenException если whole не итерабл или объекты не могут быть проверены на содержимое, например
    1 in '123'
    """
    __contains_or_not(part, whole, message=message)


def not_contains(part: Any, whole: Any, message: str = None):
    """
    Проверяется, что один объект не является частью (не входит) второго. Аналогично проверке a not in b
    :param part: объект-часть, который входит в целое
    :param whole: объект-целое, которое содержит часть
    :param message: опциональное сообщение
    :return: None
    :raises AssertionError если один объект является частью второго
    :raises TestBrokenException если whole не итерабл или объекты не могут быть проверены на содержимое, например
    1 not in '123'
    """
    __contains_or_not(part, whole, is_contains=False, message=message)


def __contains_or_not(part, whole, is_contains: bool = True, message: str = None):
    try:
        if is_contains and part in whole:
            return
        if not is_contains and part not in whole:
            return
    except TypeError as e:
        if 'requires' in e.args[0]:
            raise TestBrokenException(f'Object "{short(part)}" <{type(part).__name__}> and '
                                      f'"{short(whole)}"<{type(whole).__name__}> are of different types and cant be check '
                                      f'for contains!')
        raise TestBrokenException(
            f'"{short(whole)}"<{type(whole).__name__}> is not iterable and cant be check for contains!')
    _message = _mess(message)
    add_ = 'is a' if not is_contains else 'is not'
    raise AssertionError(f'{_message}Object "{short(part)}" <{type(part).__name__}>, {add_} part of '
                         f'"{short(whole)}"<{type(whole).__name__}>!')


def _mess(message: str) -> str:
    return f'{message}\n' if message else ''
