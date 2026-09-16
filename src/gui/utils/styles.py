from utils.output_rich import Rich


class Styler:
    """
    Класс для хранения стилей GUI приложения
    """

    def __init__(self):
        """
        создание атрибутов - цветов для стилей интерфейса
        """

        self.general_background_color: str = "#2B2D30"
        self.light_background_color: str = "#3C3F41"
        self.dark_background_color: str = "#1E1F22"


Style = Styler()
