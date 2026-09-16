from rich.console import Console


console = Console(width=200)

class RichLog:
    """
    Класс с методами вывода логов в консоль с использованием библиотеки Ruch
    """

    def __init__(self):
        pass

    def error_log(self, message: str) -> None:
        """
        Лог об ошибке (используется при сообщении об ошибке выполнении
        какой-то операции) - вывод в терминал (с использованием библиотеки Rich)

        :param message: Принимает текст сообщения об ошибке какой-то операции,
        который будет выведен в терминал (консоль)

        :return: None
        """

        console.log(f"[red][ERROR] {message}[/red]", _stack_offset=2)

    def success_log(self, message: str) -> None:
        """
        Лог об успешном выполнении (используется при сообщении об успешном выполнении
        какой-то операции) - вывод в терминал (с использованием библиотеки Rich)

        :param message: Принимает текст сообщения об успешном выполнении какой-то операции,
        который будет выведен в терминал (консоль)

        :return: None
        """

        console.log(f"[green][SUCCESS] {message}[/green]",  _stack_offset=2)

    def simple_log(self, message: str) -> None:
        """
        Обычный лог (информационный) - вывод в терминал (с использованием библиотеки Rich)

        :param message: Принимает текст лога (информационный), который будет выведен в
        терминал (консоль)

        :return: None
        """

        console.log(f"[cyan][INFO] {message}[/cyan]",  _stack_offset=2)

    def debug_log(self, message: str) -> None:
        """
        Лог для дебаггинга - вывод в терминал (с использованием библиотеки Rich)

        :param message: Принимает тест дебаг лога, который будет выведен в терминал (консоль)

        :return: None
        """

        console.log(f"[grey46][Debug] {message}[/grey46]",  _stack_offset=2)

    def warning_log(self, message: str) -> None:
        """
        Лог-предупреждение о каких-то незначительных проблемах выполнения операции
         - вывод в терминал (с использованием библиотеки Rich)

        :param message: Принимает тест лога, который будет выведен в терминал (консоль)

        :return: None
        """

        console.log(f"[bold yellow][WARN] ВНИМАНИЕ: {message}[/bold yellow]",  _stack_offset=2)

    def print_spacer(self) -> None:
        """
        Разделитель для более наглядного показа лога процессов в консоли

        :return: None
        """

        console.log(f"[grey46][Debug] {"-" * 151}[/grey46]", _stack_offset=2)

    def print_spacer_points(self) -> None:
        """
        Разделитель для более наглядного показа лога процессов в консоли -
        разделитель в виде точек

        :return: None
        """

        console.log(f"[grey46][Debug] {"." * 151}[/grey46]", _stack_offset=2)

Rich = RichLog()
