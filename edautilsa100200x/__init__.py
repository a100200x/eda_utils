"""EDA Utilities Package"""

# Импортируем функцию из вложенного модуля
from .styles.grafics import set_figure_gradient, use_style, hex_to_rgba


# Указываем, что доступно при импорте
__all__ = ['set_figure_gradient', 'use_style', 'hex_to_rgba']
__version__ = '0.1'
