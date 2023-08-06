from setuptools import setup
setup(
  name = 'transfersh-cli-config',
  py_modules=['transfersh'],
  version = '1.0.3',
  python_requires='>3.6',
  description = 'Client to upload files to the transfer.sh service',
  author = 'Maxim Semenov',
  author_email = '0rang3max@gmail.com',
  url = 'https://github.com/0rang3max/transfersh-cli-config',
  keywords = ['transfer', 'upload', 'client'],
  classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
  ),
  install_requires=[
        'Click>=6.7',
        'pyperclip>=1.6.4',
        'requests>=2.19.1',
        'appdirs>=1.4.3'
  ],
  entry_points='''
      [console_scripts]
      transfersh=transfersh:transfersh_cli
  '''
)
