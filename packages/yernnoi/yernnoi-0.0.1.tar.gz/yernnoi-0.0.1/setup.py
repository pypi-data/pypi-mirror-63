from distutils.core import setup
import os.path



setup(
  name = 'yernnoi',         # How you named your package folder (MyLib)
  packages = ['yernnoi'],   # Chose the same as "name"
  version = '0.0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Show Yernnoi Name Jaaa',   # Give a short description about your library
  long_description='',
  author = 'Yernnoi',                   # Type in your name
  author_email = 'p.boonyaplanun@gmail.com',      # Type in your E-Mail
  url = '',   # Provide either the link to your github or to your website
  download_url = '',    # I explain this later on
  keywords = ['Yernnoi'],   # Keywords that define your package best
  install_requires=[
          '',
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
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
