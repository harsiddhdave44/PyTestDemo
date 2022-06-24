import pytest

from MiracleCloud import MiracleCloud


@pytest.mark.account
def test_createAccount():
    cm = MiracleCloud()
    cm.selectCompanyAndBranchUnit(819)
    assert cm.createAccount() == True


@pytest.mark.product
def test_createProduct():
    cm = MiracleCloud()
    cm.selectCompanyAndBranchUnit(819)
    assert cm.createProduct() == True
