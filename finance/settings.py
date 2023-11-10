import configparser


conf = configparser.ConfigParser()
conf.read('settings.ini', encoding='utf-8')


class Settings:
    def __init__(self):
        self.conf = configparser.ConfigParser()
        self.conf.read('settings.ini')
        self.api_key = '7v88nf2FMxurToaCaUqTmP'
        self.api_secret = 'G0x0ELh/WnI6/bwbROgsTUz2p+DP7dK9Em4eBhOuBU8='
        self.duration = '10S'
        self.sma_duration = 5
