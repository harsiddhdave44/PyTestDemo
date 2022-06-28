import json
import random

import requests


class MiracleCloud():

    host = "https://cloud.rkitsoftware.com/mrapi/MRAPI/"

    endpoints = {
        "login": f"{host}CLCMC01/ValidateUser",
        "createCompany": f"{host}CLCMC05",
        "addAccount": f"{host}CLYMA01",
        "addProduct": f"{host}CLYMP01"
    }

    def __init__(self) -> None:
        print("Logging in")
        user = ["pc", "123"]
        print("User logged in is " + str(user))
        payload = json.dumps({
            "C01103": user[0],  # Username
            "C01104": user[1],  # Password
            "C01103R": 1
        })
        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.endpoints['login'],
                                 headers=headers,
                                 data=payload)
        resp = json.loads(response.content.decode('utf-8'))
        if ("DataModel" in resp):
            print("Logging in successful!")
            self.authToken = resp["DataModel"]["Token"]
            print("Auth Token assigned")
        else:
            print("Login failed\n" + response.content)
            raise Exception("Login to Miracle Cloud has failed. Exiting...")

# region Company Operations

    def createCompany(self):
        print("Entered 'CreateCompany'")
        print("AuthToken is" + self.authToken)
        companyNames = [
            "Linus Tech Tips", "LMG Group", "LTT Media", "BazaarKhabri.in"
        ]

        payload = json.dumps({
            "C05101": 0,
            "C05102": random.choice(companyNames),  # Company Name
            "C05103": random.randint(0, 9998)  # Company Number
        })
        headers = {
            'Authorization': f'Bearer {self.authToken}',
            'Content-Type': 'application/json'
        }
        # print(endpoints['createCompany'])
        response = requests.post(self.endpoints['createCompany'],
                                 headers=headers,
                                 data=payload)
        # print(response.content)

        # print(response.status_code)
        # print("\n\n")
        resp = response.json()
        if (resp["IsError"] == False):
            print("Company Created Successfully!")
            return True
        else:
            print("Something went wrong while creating company\n" +
                  str(response.content) + "\n")
            return False

    def setCompany(self, companyNumber):
        url = f"{self.host}CLCMC05/SetCompany?C05101={companyNumber}"

        payload = {}
        headers = {'Authorization': f'Bearer {self.authToken}'}

        response = requests.post(url, headers=headers, data=payload)

        return response.json()["DataModel"][
            "Token"]  # Returning the company auth token

    def setBranchUnit(self, token):
        url = f"{self.host}CLLogin/SetUnitBranch?B02101=1&B03101=1"

        payload = {}
        headers = {'Authorization': f'Bearer {token}'}

        response = requests.post(url, headers=headers, data=payload)
        respJson = response.json()
        print("From setBranchUnit: Token: " +
              str(respJson["DataModel"]["Token"]))
        return respJson["DataModel"]["Token"]  # Final token to be used further

    def selectCompanyAndBranchUnit(self, companyNumber):
        companyToken = self.setCompany(companyNumber)
        print("Company Selection Token:" + companyToken)
        self.authToken = self.setBranchUnit(companyToken)
        print("Final Token: " + str(self.authToken))
# endregion

# region Account Opeartions
    def createAccount(self):
        accId = random.randint(0, 999)
        dataModel = self.fetchAccDataModel()
        # setAccountIds(dataModel, accId)
        dataModel['A01102'] = f"AccountFromPytest{accId}"
        print(f"Account {dataModel['A01102']} creating")
        dataModel = json.dumps(dataModel)
        headers = {
            'Authorization': f'Bearer {self.authToken}',
            'Content-Type': 'application/json'
        }

        response = requests.post(self.endpoints['addAccount'],
                                 headers=headers,
                                 data=dataModel)
        if (response.status_code == 200):
            print("Account creation successfull!" + str(response.text))
            return True
        else:
            print("Something went wrong while creating account. Error: " +
                  str(response.content))
            return False

    def getAllAccounts(self):
        url = f"{self.host}CLYMA01/GetDDLData"

        payload = {}
        headers = {'Authorization': f'Bearer {self.authToken}'}

        response = requests.get(url, headers=headers, data=payload)

        if (response.status_code == 200):
            print("Account List fetched!")
            # Returns the list of accounts in the selected company
            return response.json()['Data']
        else:
            print("Couldn't fetch the accounts list, exiting")
            return False
# endregion

# region Prodcut Operations
    def createProduct(self):
        url = f"{self.host}/mrapi/MRAPI/CLYMP01"

        dataModel = self.fetchProdDataModel()
        dataModel['P01102'] = f'AddedFromPy{random.randint(0, 9999)}'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.authToken}'
        }

        response = requests.post(self.endpoints["addProduct"],
                                 headers=headers,
                                 data=json.dumps(dataModel))
        if (response.status_code == 200):
            print("Product added")
            return True
        else:
            print(f"Error adding product. Message: {response.text}")
            return False

    def getAllProducts(self):
        url = f"{self.host}CLYMP01/GetDDLData"

        headers = {'Authorization': f'Bearer {self.authToken}'}

        response = requests.get(url, headers=headers)

        productList = response.json()['Data']
        if (response.status_code == 200 and productList != None):
            return productList
        else:
            print(f"Error fetching products, Message: {response.text}")
            return False

    def editProduct(self):
        url = f"{self.host}CLYMP01"
        prodId = random.choice(self.getAllProducts())['P01101']
        print(f"Selected product id {prodId} for editing\n")
        dataModel = self.fetchProdDataModel()
        self.setProductIds(dataModel, prodId)
        dataModel[
            'P01102'] = f"ProductChangedFromPytest{prodId}{random.randint(0, 9999)}"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.authToken}'
        }

        response = requests.put(url,
                                headers=headers,
                                data=json.dumps(dataModel))
        if (response.status_code == 200):
            print(f"Edited the product {dataModel['P01102']} succefully!")
            return True
        else:
            print(f"Failed to edit the product. \nError {response.text}")
            return False

    def deleteProduct(self):
        prodId = random.choice(self.getAllProducts())['P01101']
        url = f"{self.host}CLYMP01?id={prodId}"

        headers = {'Authorization': f'Bearer {self.authToken}'}
        response = requests.delete(url, headers=headers)
        if (response.status_code == 200):
            print("Deleted product successfully")
            return True
        else:
            print(f"Error fetching products, Message: {response.text}")
            return False
# endregion

# region Helpers
    def setProductIds(self, dataModel, prodId):
        dataModel['P01101'] = prodId
        dataModel['DTOYMP03']['P03102'] = prodId
        dataModel['DTOYMP06']['P06101'] = prodId

    def fetchProdDataModel(self):
        with open("ProductModel.json", "r") as dataModelFile:
            jsonModel = json.load(dataModelFile)
            return jsonModel

    def fetchAccDataModel(self):
        with open("AddAccountModel.json", "r") as dataModelFile:
            jsonModel = json.load(dataModelFile)
            return jsonModel
# endregion
