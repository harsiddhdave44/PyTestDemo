import pytest

from MiracleCloud import MiracleCloud

companyId = 1213


@pytest.mark.account
@pytest.mark.createOperations
def test_createAccount():
    cm = MiracleCloud()
    cm.selectCompanyAndBranchUnit(companyId)
    assert cm.createAccount() == True


@pytest.mark.account
@pytest.mark.readOperations
def test_getAllAccounts():
    cm = MiracleCloud()
    cm.selectCompanyAndBranchUnit(companyId)
    assert True if cm.getAllAccounts() != None else False


# region Product Operations


@pytest.mark.product
@pytest.mark.createOperations
def test_createProduct():
    cm = MiracleCloud()
    cm.selectCompanyAndBranchUnit(companyId)
    assert cm.createProduct() == True


@pytest.mark.product
@pytest.mark.readOperations
def test_getAllProducts():
    cm = MiracleCloud()
    cm.selectCompanyAndBranchUnit(companyId)
    # If product list is not empty, return True, otherwise False
    assert True if cm.getAllProducts() != None else False


@pytest.mark.product
def test_editProduct():
    cm = MiracleCloud()
    cm.selectCompanyAndBranchUnit(companyId)
    assert cm.editProduct()


@pytest.mark.product
def test_deleteProduct():
    cm = MiracleCloud()
    cm.selectCompanyAndBranchUnit(companyId)
    assert cm.deleteProduct()

# endregion
