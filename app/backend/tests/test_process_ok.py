import pytest


@pytest.fixture
def tx_hash():
    return '0x0ba5abf4ef9eedb75a7fd5e645034288e02c6c4fafebf932e191b4df1f8ffac8'


@pytest.fixture
def expected_result():
    return {"hash": "0x0ba5abf4ef9eedb75a7fd5e645034288e02c6c4fafebf932e191b4df1f8ffac8",
            "fromAddress": "0x0057Be07BEEF5D9B4Beb9e2d147906e83d1915C8",
            "toAddress": "0x8f26D7bAB7a73309141A291525C965EcdEa7Bf42", "blockNumber": 15077724,
            "executedAt": "2022-07-04T18:40:00", "gasUsed": 186594, "gasCostInDollars": 0.2}


@pytest.mark.asyncio
async def test_process_transaction_hash(client, tx_hash, expected_result):
    response = await client.get(f"/transactions/{tx_hash}")
    assert response.status_code == 200
    assert response.json() == expected_result
