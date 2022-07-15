from datetime import datetime


def gwei_to_eth():
    return 0.000000001


async def from_address(receipt):
    return receipt.get('from')


async def to_address(receipt):
    return receipt.get('to')


async def block_number(receipt):
    return receipt.get('blockNumber')


async def eth_hist_price(date, cg):
    eth_hist_price = cg.get_coin_history_by_id(id='ethereum', date=date.strftime('%d-%m-%Y'), localization='false')
    return eth_hist_price["market_data"]["current_price"]["usd"]


async def gas_cost_in_dollars(receipt, block_info, cg):
    gas_cost_gwei = await gas_cost(receipt)
    gas_cost_eth = gas_cost_gwei * gwei_to_eth()
    date = await execution_timestamp_from_block_info(block_info)
    eth_to_usd = await eth_hist_price(date, cg)
    return round(gas_cost_eth * eth_to_usd, 2)


async def tx_receipt(tx_hash, w3):
    return w3.eth.get_transaction_receipt(tx_hash)


async def tx_block_info(receipt, w3):
    return w3.eth.get_block(receipt.get('blockNumber'))


async def execution_timestamp_from_block_info(block_info):
    ts = block_info.timestamp
    return datetime.utcfromtimestamp(ts)


async def gas_cost(receipt):
    return receipt.get('gasUsed')
