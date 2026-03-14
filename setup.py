from setuptools import setup

setup(name='edautilsa100200x',
      version='0.2',
      description='EDA_utilities',
      packages=['edautilsa100200x'],
      author_email='author@gmail.com',
      package_data={'edautilsa100200x': ['*', '**/*'],},  # ВКЛЮЧИТЬ ВСЁ!
      install_requires=['numpy', 'matplotlib'],  # Добавить зависимости
      zip_safe=False)
