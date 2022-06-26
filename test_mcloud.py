import pytest

from MiracleCloud import MiracleCloud


@pytest.mark.account
def test_createAccount():
    cm = MiracleCloud()
    cm.selectCompanyAndBranchUnit(1213)
    assert cm.createAccount() == True


@pytest.mark.product
def test_createProduct():
    cm = MiracleCloud()
    cm.selectCompanyAndBranchUnit(1213)
    assert cm.createProduct() == True
