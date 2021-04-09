#!/usr/bin/env python3
import iterm2
import aiohttp
import time
import random


SYMBOLS = {
    "ETH": "⧫",
    "BCH": "₿c",
    "LTC": "Ł",
    "BTC": "₿",
}

UP = "▲"
DOWN = "▼"

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774"


async def get_price(coin):
    if coin not in SYMBOLS:
        raise ValueError(f"Coin must be one of {'|'.join(SYMBOLS.keys())}")
    async with aiohttp.ClientSession() as session:
        t = int(time.time()) - 1
        r = random.randint(100, 999)
        eth_url = f'https://api.ethereumdb.com/v1/ticker?pair={coin}-USD&range=24h&t={t}{r}'
        async with session.get(eth_url, headers={'User-Agent': UA}) as resp:
            data = await resp.json()

    return data


async def main(connection):
    # Define the configuration knobs:
    coins = list(SYMBOLS.keys())
    knobs = []
    for coin in coins:
        knob = iterm2.CheckboxKnob(coin, True, coin)
        knobs.append(knob)

    knobs.append(iterm2.CheckboxKnob('show price', True, 'price'))
    data_opts = ['high', 'low', 'change', 'changePercent', 'open']
    for opt in data_opts:
        knobs.append(iterm2.CheckboxKnob(f'show {opt}', False, opt))
    component = iterm2.StatusBarComponent(
        short_description="Show crypto tickers in the status bar",
        detailed_description="Show the price, changes, and other data about various cryto coins in the status bar. "
        f"Updates every 10 seconds. Supported coins are {' '.join(SYMBOLS)}",
        knobs=knobs,
        exemplar="Crypto Ticker",
        update_cadence=10,
        identifier="com.spyoung.crypto-ticker",
    )

    @iterm2.StatusBarRPC
    async def coro(knobs):
        prices = []
        for coin in coins:
            if coin in knobs and knobs[coin]:
                price_data = await get_price(coin)
                prices.append(price_data)

        # format the data according to settings
        strings = []
        for price_data in prices:
            pair = price_data['pair']
            coin = pair.split('-')[0]

            s = f'{SYMBOLS[coin]}'
            if 'price' in knobs and knobs['price']:
                price = round(price_data['price'], 4)
                s += f' {pair}: ${price}'
            for opt in ['high', 'low', 'open']:
                if opt in knobs and knobs[opt]:
                    s += f' {opt}: ${price_data.get(opt, "ERR")}'
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

            strings.append(s)

        # Provide various sizes that will show/hide according to window width
        rets = [' | '.join(strings), *strings]
        for i in range(2, len(strings)):
            group = strings[0:i]
            rets.append(' | '.join(group))
        without_pairs = ' | '.join(strings)
        for p in prices:
            without_pairs = without_pairs.replace(p['pair'], '')
        rets.append(without_pairs)
        rets.sort(key=len, reverse=True)
        return rets

    # Register the component.
    await component.async_register(connection, coro)


iterm2.run_forever(main)
