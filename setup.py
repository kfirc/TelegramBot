from setuptools import setup, find_packages

setup(
    name='TelegramBot',
    version='1',
    description='A tool to control and maintain telegram bots',
    url='https://github.com/kfirc/TelegramBot',
    author='Kfir Cohen',
    author_email='kfir969@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'python-telegram-bot==12.8',
    ],
)
