from setuptools import setup

setup(
   name='randcolor',
   version='1.0.2',
   description='Make a map',
   author='FuryBaM',
   author_email='furybam@gmail.com',
   packages=['randcolor'],  #same as name
   install_requires=['Pillow', 'tqdm', 'numpy'], #external packages as dependencies
   scripts=['randcolor/menu.py'],
   package_data={'randcolor': ['img.png']},
   include_package_data=True,
   entry_points={ 'console_scripts': ['randcolor=randcolor.menu:start' ] },
   url="https://github.com/FuryBaM/randcolor",
)