#!/usr/bin/env python3
import iterm2
import aiohttp
import time
import random
from collections import defaultdict
import copy
import asyncio
print('starting')
COIN_SYMBOLS = defaultdict(str)

COIN_SYMBOLS.update(
    {
        "ETH": "⧫",
        "BCH": "₿c",
        "LTC": "Ł",
        "BTC": "₿",
    }
)


CURRENCY_SYMBOLS = defaultdict(lambda: "$")
CURRENCY_SYMBOLS.update(copy.deepcopy(COIN_SYMBOLS))
CURRENCY_SYMBOLS.update({'EUR': '€', 'JPY': '¥', 'GBP': '£', 'USD': '$'})


UP = "▲"
DOWN = "▼"

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774"


def _make_key(args, kwargs):
    """
    Variation of functools._make_key
    """
    _kwd_mark = (object(),)
    key = args
    if kwargs:
        key += _kwd_mark
        for item in kwargs.items():
            key += item
    return tuple(key)

class CacheInfo:
    def __init__(self):
        self.hits = 0
        self.misses = 0

def timed_cache(ttl: int = 10, maxsize: int = 100):
    """
    Variation of functools.lru_cache, but expires with time.
    """
    if maxsize:
        assert maxsize > 0
    result_cache = {}
    cache_info = CacheInfo()
    cache_lock = asyncio.Lock()
    def deco(f):
        async def wrapper(*args, _ttl=None, **kwargs):
            nonlocal result_cache
            nonlocal cache_info
            if _ttl is None:
                _ttl = ttl
            key = _make_key(args, kwargs)
            async with cache_lock:
                if key in result_cache:
                    expiration, result = result_cache[key]
                    if time.time() < expiration:
                        print('cache hit', key)
                        cache_info.hits += 1
                        return result
                    else:
                        result_cache.pop(key)
                print('cache miss', key)
                print('Hits:', cache_info.hits, "Misses:", cache_info.misses)
                cache_info.misses += 1
                expiration = time.time() + _ttl
                result = await f(*args, **kwargs)
            if maxsize and len(result_cache) >= maxsize:
                result_cache.pop(list(result_cache)[0])
            result_cache[key] = (expiration, result)
            return result
        wrapper.cache_info = cache_info
        return wrapper
    return deco

session = None

@timed_cache(ttl=10, maxsize=100)
async def get_price(coin: str, currency="USD", ticker_range="24h"):
    global session
    if session is None:
        session = aiohttp.ClientSession()
    t = int(time.time()) - 1
    r = random.randint(100, 999)
    eth_url = f'https://api.ethereumdb.com/v1/ticker?pair={coin}-{currency}&range={ticker_range}&t={t}{r}'
    print('req start', eth_url)
    async with session.get(eth_url, headers={'User-Agent': UA}) as resp:
        resp.raise_for_status()
        data = await resp.json()
    print('req done', eth_url)
    return data


async def main(connection):
    # Define the configuration knobs:
    knobs = [
        iterm2.StringKnob('Coin (e.g. "BTC")', "ETH", "ETH", "coin"),
        iterm2.StringKnob('Currency (e.g. "USD")', "USD", "USD", "currency"),
        iterm2.StringKnob('range (10mi,1h,12h,24h,1w,1m,3m,1y,ytd,all)', "24h", "24h", "ticker_range"),
        iterm2.PositiveFloatingPointKnob("Update interval (seconds)", 10, "update_interval")
    ]

    knobs.append(iterm2.CheckboxKnob('show price', True, 'price'))

    data_opts = ['high', 'low', 'change', 'changePercent', 'open']
    for opt in data_opts:
        knobs.append(iterm2.CheckboxKnob(f'show {opt}', False, opt))
    component = iterm2.StatusBarComponent(
        short_description="Show crypto tickers in the status bar",
        detailed_description="Show the price, changes, and other data about a given cryto coins in the status bar. "
        f"Updates every 10 seconds. Uses ethereumdb api",
        knobs=knobs,
        exemplar="Crypto Ticker",
        update_cadence=None,
        identifier="com.spyoung.crypto-ticker",
    )

    @iterm2.StatusBarRPC
    async def coro(knobs):
        if 'coin' in knobs:
            coin = knobs['coin']
        else:
            coin = 'ETH'

        if 'currency' in knobs:
            currency = knobs['currency']
        else:
            currency = 'USD'
        if "ticker_range" in knobs:
            ticker_range = knobs['ticker_range']
        else:
            ticker_range = "24h"
        if 'update_interval' in knobs and knobs['update_interval']:
            ttl = int(knobs['update_interval'])
            if ttl <= 0:
                ttl = 10
            ttlkwd = {'_ttl': ttl}
        else:
            ttlkwd = {}

        price_data = await get_price(coin, currency, ticker_range, **ttlkwd)
        # format the data according to settings
        pair = price_data['pair']
        currency_symbol = CURRENCY_SYMBOLS.get(currency, '$')

        s = f'{COIN_SYMBOLS[coin]}'
        if 'price' in knobs and knobs['price']:
            price = round(price_data['price'], 4)
            s += f' {pair}: {currency_symbol}{price}'
        for opt in ['high', 'low', 'open']:
            if opt in knobs and knobs[opt]:
                s += f' {opt}: {currency_symbol}{price_data.get(opt, "ERR")}'
        if ('change' in knobs and knobs['change']) or ('changePercent' in knobs and knobs['changePercent']):
            if price_data['change'] >= 0:
                symbol = UP
            else:
                symbol = DOWN
            cs = f'{symbol}'
            if 'change' in knobs and knobs['change']:
                change = round(price_data['change'], 3)
                cs += f' {currency_symbol}{change}'
            if 'changePercent' in knobs and knobs['changePercent']:
                change_percent = round(price_data['changePercent'], 4)
                cs += f' {change_percent}%'
            s += f' {cs}'

        if COIN_SYMBOLS[coin]:
            # Allow a smaller display without the pair (e.g. ETH-USD)
            # But only when there is an existing symbol
            without_pair = s.replace(f" {pair}", '')
            return [s, without_pair]
        return s

    # Register the component.
    await component.async_register(connection, coro)

print('running')
iterm2.run_forever(main)
