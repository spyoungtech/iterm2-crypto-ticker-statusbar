#!/usr/bin/env python3
import iterm2
import aiohttp
import time
import random
from collections import defaultdict
import copy
COIN_SYMBOLS = defaultdict(str)

COIN_SYMBOLS.update({
    "ETH": "⧫",
    "BCH": "₿c",
    "LTC": "Ł",
    "BTC": "₿",
})


CURRENCY_SYMBOLS = defaultdict(lambda: "$")
CURRENCY_SYMBOLS.update(copy.deepcopy(COIN_SYMBOLS))
CURRENCY_SYMBOLS.update({'EUR': '€', 'JPY': '¥', 'GBP': '£', 'USD': '$'})



UP = "▲"
DOWN = "▼"

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774"


async def get_price(coin, currency="USD"):
    async with aiohttp.ClientSession() as session:
        t = int(time.time()) - 1
        r = random.randint(100, 999)
        eth_url = f'https://api.ethereumdb.com/v1/ticker?pair={coin}-{currency}&range=24h&t={t}{r}'
        async with session.get(eth_url, headers={'User-Agent': UA}) as resp:
            resp.raise_for_status()
            data = await resp.json()
    return data


async def main(connection):
    # Define the configuration knobs:
    coins = list(COIN_SYMBOLS.keys())
    knobs = [iterm2.StringKnob('Coin (e.g. "BTC")', "ETH", "ETH", "coin"),
             iterm2.StringKnob('Currency (e.g. "USD")', "USD", "USD", "currency")
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
        update_cadence=10,
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
        price_data = await get_price(coin, currency)
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
                cs += f' ${change}'
            if 'changePercent' in knobs and knobs['changePercent']:
                change_percent = round(price_data['changePercent'], 4)
                cs += f' {change_percent}%'
            s += f' {cs}'


        without_pair = s.replace(price_data['pair'], '')
        return [s, without_pair]

    # Register the component.
    await component.async_register(connection, coro)


iterm2.run_forever(main)
