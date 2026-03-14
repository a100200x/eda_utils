"""EDA Utilities Package"""

# Импортируем функцию из вложенного модуля
from .styles.grafics import set_figure_gradient
import os

def use_style(style_name='style_1'):
    """Применить стиль matplotlib из пакета"""
    style_path = os.path.join(os.path.dirname(__file__), 'styles', f'{style_name}.mplstyle')
    if os.path.exists(style_path):
        plt.style.use(style_path)
        print(f"Стиль {style_name} применен")
    else:
        print(f"Стиль {style_name} не найден")

# Указываем, что доступно при импорте
__all__ = ['set_figure_gradient']
__version__ = '0.1'
