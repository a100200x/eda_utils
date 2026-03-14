import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
import matplotlib.patches as patches

def set_figure_gradient(fig, 
                        colors=None,           # список цветов (от 2 до 10)
                        direction='vertical',  # vertical/horizontal/diagonal/radial/corner
                        cmap_name=None,        # имя встроенной карты (viridis, plasma, etc.)
                        alpha=0.8,             # прозрачность
                        noise=0,                # шум (0-1) для текстуры
                        pattern=None,           # 'stripes', 'dots', 'waves'
                        blend_mode='normal'):   # normal/multiply/screen/overlay
    """
    Универсальная функция для создания градиентного фона фигуры
    
    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        Фигура
    colors : list
        Список цветов (hex или rgb). Если None, используется cmap_name
    direction : str
        'vertical', 'horizontal', 'diagonal', 'radial', 'corner'
    cmap_name : str
        Имя встроенной цветовой карты (viridis, plasma, coolwarm, etc.)
    alpha : float
        Прозрачность (0-1)
    noise : float
        Добавляет шум/текстуру (0 - нет, 1 - максимум)
    pattern : str
        Наложить узор: 'stripes', 'dots', 'waves'
    blend_mode : str
        Режим смешивания (экспериментально)
    """
    
    # Получаем размер фигуры в пикселях
    bbox = fig.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width_inch, height_inch = bbox.width, bbox.height
    width_px = int(width_inch * fig.dpi)
    height_px = int(height_inch * fig.dpi)
    
    # Создаем базовую сетку для градиента
    if direction == 'vertical':
        # От верха к низу
        gradient = np.linspace(0, 1, height_px).reshape(-1, 1)
        gradient = np.tile(gradient, (1, width_px))
        
    elif direction == 'horizontal':
        # От левого края к правому
        gradient = np.linspace(0, 1, width_px).reshape(1, -1)
        gradient = np.tile(gradient, (height_px, 1))
        
    elif direction == 'diagonal':
        # От верхнего левого к нижнему правому
        x = np.linspace(0, 1, width_px)
        y = np.linspace(0, 1, height_px)
        X, Y = np.meshgrid(x, y)
        gradient = (X + Y) / 2
        
    elif direction == 'radial':
        # От центра к краям
        x = np.linspace(-1, 1, width_px)
        y = np.linspace(-1, 1, height_px)
        X, Y = np.meshgrid(x, y)
        gradient = np.sqrt(X**2 + Y**2)
        gradient = gradient / gradient.max()  # нормируем
        
    elif direction == 'corner':
        # От угла (верхнего левого)
        x = np.linspace(0, 1, width_px)
        y = np.linspace(0, 1, height_px)
        X, Y = np.meshgrid(x, y)
        gradient = np.sqrt(X**2 + Y**2) / np.sqrt(2)
    
    elif direction == 'triangular':
        # Треугольный градиент
        x = np.linspace(0, 1, width_px)
        y = np.linspace(0, 1, height_px)
        X, Y = np.meshgrid(x, y)
        gradient = 1 - np.abs(X - Y)
    
    # Добавляем шум для текстуры
    if noise > 0:
        noise_pattern = np.random.rand(height_px, width_px) * noise
        gradient = gradient * (1 - noise) + noise_pattern * noise
    
    # Добавляем узоры
    if pattern == 'stripes':
        stripe = np.sin(np.linspace(0, 20*np.pi, width_px))
        stripe = (stripe + 1) / 2  # нормируем в 0-1
        stripe = np.tile(stripe, (height_px, 1))
        gradient = (gradient + stripe) / 2
        
    elif pattern == 'dots':
        x = np.linspace(0, 10*np.pi, width_px)
        y = np.linspace(0, 10*np.pi, height_px)
        X, Y = np.meshgrid(x, y)
        dots = (np.sin(X) * np.sin(Y) + 1) / 2
        gradient = (gradient + dots) / 2
        
    elif pattern == 'waves':
        x = np.linspace(0, 10*np.pi, width_px)
        y = np.linspace(0, 10*np.pi, height_px)
        X, Y = np.meshgrid(x, y)
        waves = (np.sin(X + Y) + 1) / 2
        gradient = (gradient + waves) / 2
    
    # Создаем цветовую карту
    if colors:
        # Конвертируем hex в rgb если нужно
        rgb_colors = []
        for color in colors:
            if isinstance(color, str):
                if color.startswith('#'):
                    rgb = tuple(int(color.lstrip('#')[i:i+2], 16)/255 for i in (0, 2, 4))
                    rgb_colors.append(rgb)
                else:
                    # Название цвета
                    from matplotlib.colors import to_rgb
                    rgb_colors.append(to_rgb(color))
            else:
                rgb_colors.append(color)
        
        cmap = LinearSegmentedColormap.from_list('custom_gradient', rgb_colors)
    
    elif cmap_name:
        cmap = plt.get_cmap(cmap_name)
    
    else:
        # По умолчанию - от вашего цвета #9093A2 к белому
        default_color = (0.5647, 0.5765, 0.6353)
        cmap = LinearSegmentedColormap.from_list('default', [default_color, (1,1,1)])
    
    # Применяем градиент
    if blend_mode == 'normal':
        fig.figimage(gradient, cmap=cmap, origin='upper', alpha=alpha, zorder=-1)
    else:
        # Для других режимов смешивания нужен более сложный подход
        from matplotlib.colors import Normalize
        norm = Normalize(vmin=0, vmax=1)
        rgba = cmap(norm(gradient))
        
        # Применяем режим смешивания (упрощенно)
        if blend_mode == 'multiply':
            rgba[..., :3] *= 0.8
        elif blend_mode == 'screen':
            rgba[..., :3] = 1 - (1 - rgba[..., :3]) * 0.7
        
        fig.figimage(rgba, origin='upper', zorder=-1)
    
    # Делаем все оси прозрачными
    for ax in fig.get_axes():
        ax.set_facecolor('none')
        ax.patch.set_alpha(0)
    
    return fig

def use_style(style_name='style_1'):
    """Применить стиль matplotlib из пакета"""
    style_path = os.path.join(os.path.dirname(__file__), 'styles', f'{style_name}.mplstyle')
    if os.path.exists(style_path):
        plt.style.use(style_path)
        print(f"Стиль {style_name} применен")
    else:
        print(f"Стиль {style_name} не найден")
