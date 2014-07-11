import sys


class Card_config(object):
    """Первоначальные настройки для класса Card"""
    if sys.stdout.encoding == 'cp866':  # Консоль windows
        suits = [chr(3), chr(4), chr(5), chr(6)]
    elif sys.stdout.encoding == 'UTF-8':  # unix
        suits = [chr(0x2665), chr(0x2666), chr(0x2663), chr(0x2660)]
    elif sys.stdout.encoding == 'cp1251':  # GUI windows
        suits = ['h', 'd', 'c', 's']
    vals = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
