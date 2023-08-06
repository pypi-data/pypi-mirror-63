import traceback
import time

from .basic_case import TestCase
from .basic_group import TestGroup
from .basic_suite import TestSuite
from checking.helpers.exception_traceback import get_trace_filtered_by_filename


def _print_splitter_line():
    print('-' * 10)


def short(object) -> str:
    return _short(str(object), width=50)


def _short(x, width: int = 10):
    string = str(x)
    if len(string) > width:
        return string[:45] + '[...]'
    return string


class Listener:
    """
    Родитель слушателей тестов. Пользователь может написать свой слушатель и изменить поведение по-умолчанию, при этом
    его слушатель должен быть наследником данного класса.
    """

    def __init__(self, verbose: int = 0):
        self.verbose = verbose

    def on_suite_starts(self, test_suite: TestSuite):
        """
        Вызывается при старте прогона, после проверки провайдеров
        :param test_suite: TestSuite
        :return: None
        """
        pass

    def on_suite_ends(self, test_suite: TestSuite):
        """
        Вызывается при завершении прогона, когда уже завершены все тесты и фикстуры
        :param test_suite: TestSuite
        :return: None
        """
        pass

    def on_test_starts(self, test: TestCase, group: TestGroup):
        """
        Вызывается перед стартом теста (уже после предварительных фикстур, но до самого теста).
        :param test: объект теста со всеми параметрами
        :param group: группа, к которой тест принадлежит
        :return: None
        """
        pass

    def on_empty_suite(self, test_suite: TestSuite):
        """
        Вызывается перед остановкой прогона в связи с тем, что нет тестов ни в одной из групп.
        :param test_suite: TestSuite
        :return: None
        """
        pass

    def on_fixture_failed(self, group_name: str, fixture_type: str, exception_: Exception):
        """
        Вызывается при неудачном запуске фикстуры (before/after)
        :param group_name: имя группы тестов
        :param fixture_type: название фикстуры
        :param exception_: упавшее исключение
        :return: None
        """
        pass

    def on_ignored_with_provider(self, test: TestCase, group: TestGroup):
        """
        Вызывается, когда функция, помеченная как @data не возвращает Iterable и все тесты, привязанные к данному
        провайдеру игнорируются
        :param test: TestCase
        :param group: TestGroup
        :return: None
        """
        self._to_results(group, test, 'ignored')

    def on_success(self, group: TestGroup, test: TestCase):
        """
        Вызывается, когда тест завершен успешно
        :param group: TestGroup
        :param test: TestCase
        :return: None
        """
        self._to_results(group, test, 'success')

    def on_failed(self, group: TestGroup, test: TestCase, exception_: Exception):
        """
        Вызывается при падении теста по ассерту (встроенному или из модуля checking.asserts)
        :param group: TestGroup
        :param test: TestCase
        :param exception_: упавший ассерт
        :return: None
        """
        self._to_results(group, test, 'failed')

    def on_broken(self, group: TestGroup, test: TestCase, exception_: Exception):
        """
        Вызывается, когда тест "сломан", то есть падает с исключением, а не по ассерту
        :param group: TestGroup
        :param test: TestCase
        :param exception_: упавшее исключение
        :return: None
        """
        self._to_results(group, test, 'broken')

    def on_ignored(self, group: TestGroup, test: TestCase, fixture_type: str):
        """
        Вызывается, когда тест проигнорирован из-за упавшей фикстуры (before)
        :param group: TestGroup
        :param test: TestCase
        :param fixture_type: название фикстуры, вызвавшей игнорирование
        :return: None
        """
        self._to_results(group, test, 'ignored')

    def _to_results(self, group: TestGroup, test: TestCase, result: str):
        group.add_result_to(test, result)

    def on_before_suite_failed(self, test_suite):
        """
        Вызывается при падении @before_suite фикстуры
        :param test_suite: TestSuite
        :return: None
        """
        pass


class DefaultListener(Listener):
    """
    Слушатель по-умолчанию для стандартного поведения при событиях прогона.
    Пользователь может написать свои собственные слушатели по образцу данного класса.
    """

    def on_before_suite_failed(self, test_suite):
        super().on_before_suite_failed(test_suite)
        print(f'Before suite "{test_suite.name}" failed! Process stopped!')

    def on_suite_starts(self, test_suite: TestSuite):
        super().on_suite_starts(test_suite)
        self.start_time = time.time()

    def on_empty_suite(self, test_suite: TestSuite):
        print('No tests were found! Stopped...')

    def on_suite_ends(self, test_suite: TestSuite):
        super().on_suite_ends(test_suite)
        if not self.verbose:
            print()
        print()
        print("=" * 30)
        elapsed = time.time() - self.start_time
        success_count = len(test_suite.success())
        f_count = len(test_suite.failed())
        b_count = len(test_suite.broken())
        i_count = len(test_suite.ignored())
        all_count = f_count + b_count + i_count + success_count
        print(f'Total tests:{all_count}, success tests : {success_count}, failed tests:{f_count}, broken tests:'
              f'{b_count}, ignored tests:{i_count}')
        print(f'Time elapsed: {elapsed:.2f} seconds.')
        if self.verbose == 3:
            if f_count:
                print(f'\nFailed tests are:')
                for failed_test in test_suite.failed():
                    print(' ' * 4, failed_test)
            if b_count:
                print(f'\nBroken tests are:')
                for broken_test in test_suite.broken():
                    print(' ' * 4, broken_test)
            if i_count:
                print(f'\nIgnored tests are:')
                for ignored_test in test_suite.ignored():
                    print(' ' * 4, ignored_test)
        print("=" * 30)

    def on_success(self, group: TestGroup, test: TestCase):
        super().on_success(group, test)
        if not self.verbose:
            print('.', end='')
        elif self.verbose > 1:
            _print_splitter_line()
            print(f'"{test}" SUCCESS!')

    def on_broken(self, group: TestGroup, test: TestCase, exception_: Exception):
        super().on_broken(group, test, exception_)
        self._failed_or_broken(test, exception_, 'broken')

    def on_failed(self, group: TestGroup, test: TestCase, exception_: Exception):
        super().on_failed(group, test, exception_)
        self._failed_or_broken(test, exception_, 'failed')

    def on_ignored(self, group: TestGroup, test: TestCase, fixture_type: str):
        super().on_ignored(group, test, fixture_type)
        print(f'Because of fixture "{fixture_type}" tests {test} was IGNORED!')
        _print_splitter_line()

    def on_fixture_failed(self, group_name: str, fixture_type: str, exception_: Exception):
        super().on_fixture_failed(group_name, fixture_type, exception_)
        _print_splitter_line()
        print(f'Fixture {fixture_type} "{group_name}" failed!')
        for tb in (e for e in traceback.extract_tb(exception_.__traceback__)):
            print(f'File "{tb.filename}", line {tb.lineno}, in {tb.name}')
        print(exception_)

    def on_ignored_with_provider(self, test: TestCase, group: TestGroup):
        super().on_ignored_with_provider(test, group)
        print(f'Provider "{test.provider}" for {test} not returns iterable! All tests with provider were IGNORED!')

    def on_test_starts(self, test: TestCase, group: TestGroup):
        super().on_test_starts(test, group)

    def _failed_or_broken(self, test, exception_, _result):
        _letter = f'{_result.upper()}!'
        if not self.verbose:
            print(_letter[0], end='')
        else:
            if self.verbose > 0:
                _print_splitter_line()
            print(f'Test {test} {_letter}')
            print(get_trace_filtered_by_filename(exception_))
            print(exception_)
