import datetime
from mongokit import Document
from rex import app, db
import validators

__author__ = 'taijoe'


class Ticker(Document):
    __collection__ = 'ticker'

    structure = {
        'btc_usd' : float,
        'eth_usd' : float,
        'bth_usd' : float,
        'ltc_usd' : float,
        'coin_usd' : float,
        'xrp_usd' : float,
        'dash_usd' : float,
        'usdt_usd' : float,
        'doge_usd' : float,
        'bch_usd' : float,

        'btc_change' : float,
        'eth_change' : float,
        'ltc_change' : float,
        'eos_change' : float,
        'dash_change' : float,
        'usdt_change' : float,
        'coin_change' : float,
        'xrp_change' : float,
        'doge_change' : float,
        'bch_change' : float
    }
    default_values = {
        'btc_usd' : 0,
        'eth_usd' : 0,
        'bth_usd' : 0,
        'ltc_usd' : 0,
        'coin_usd' : 0,
        'xrp_usd' : 0,
        'dash_usd' : 0,
        'usdt_usd' : 0,
        'doge_usd' : 0,
        'bch_usd' : 0,

        'btc_change' : 0,
        'eth_change' : 0,
        'ltc_change' : 0,
        'eos_change' : 0,
        'dash_change' : 0,
        'usdt_change' : 0,
        'coin_change' : 0,
        'xrp_change' : 0,
        'doge_change' : 0,
        'bch_change' : 0
    }
    use_dot_notation = True

db.register([Ticker])