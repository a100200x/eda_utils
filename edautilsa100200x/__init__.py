"""EDA Utilities Package"""

# Импортируем функцию из вложенного модуля
from .styles.grafics import set_figure_gradient, use_style



# Указываем, что доступно при импорте
__all__ = ['set_figure_gradient', 'use_style']
__version__ = '0.1'
