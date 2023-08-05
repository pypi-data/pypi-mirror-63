from distutils.core import setup
from setuptools import setup, find_packages
import pathlib
setup(
  name = 'gray_box_clf',         # How you named your package folder (MyLib)
  packages=find_packages(),
  version = '0.2.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'classificaion witout wax',   # Give a short description about your library
  author = 'Adam H. Agbaria',                   # Type in your name
  author_email = 'adam.h.agb@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/AdamHamody/sincera_gray_box',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/AdamHamody/sincera_gray_box/archive/0.0.1.tar.gz',    # I explain this later on
  keywords = ['chi2', 'classification'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'matplotlib','iminuit', "scipy", 'numpy', "pandas","pyod", "sklearn", "xgboost", "catboost", "lightgbm"
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],

  include_package_data=True,

)
