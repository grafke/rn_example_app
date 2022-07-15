import logging.config
from datetime import datetime
from decimal import Decimal
from web3 import Web3
from pycoingecko import CoinGeckoAPI

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.backend.config import LOGGING, WEB3_HTTP_PROVIDER
from app.backend.processor.eth_transaction_processor import from_address, to_address, block_number, \
    gas_cost_in_dollars, tx_receipt, tx_block_info, execution_timestamp_from_block_info, gas_cost

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('app')

app = FastAPI()

w3 = Web3(Web3.HTTPProvider(WEB3_HTTP_PROVIDER))
cg = CoinGeckoAPI()


class BasicResponse(BaseModel):
    hash: str
    fromAddress: str
    toAddress: str
    blockNumber: int
    executedAt: datetime
    gasUsed: int
    gasCostInDollars: Decimal


@app.get("/transactions/{hash}", response_model=BasicResponse)
async def process_transaction_hash(hash):
    logger.info(hash)
    receipt_info = await tx_receipt(hash, w3)
    block_info = await tx_block_info(receipt_info, w3)
    result = {
        "hash": hash,
        "fromAddress": await from_address(receipt_info),
        "toAddress": await to_address(receipt_info),
        "blockNumber": await block_number(receipt_info),
        "executedAt": await execution_timestamp_from_block_info(block_info),
        "gasUsed": await gas_cost(receipt_info),
        "gasCostInDollars": await gas_cost_in_dollars(receipt_info, block_info, cg),
    }
    logger.info(result)
    return result


@app.get("/")
async def main():
    content = """OK"""
    return HTMLResponse(content=content)
