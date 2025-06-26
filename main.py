# a fastapi system for account managament

import os
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date

app = FastAPI()

class Account(BaseModel):
    id: int
    type: str
    person_name: str
    adress: str


ACCOUNTS_FILE = "accounts.txt"

def write_account_to_file(account: Account):
    with open(ACCOUNTS_FILE, "a") as file:
        file.write(f"{account.id},{account.type},{account.person_name},{account.adress}\n")

def read_accounts_from_file():
    accounts = []
    if not os.path.exists(ACCOUNTS_FILE):
        return accounts
    with open(ACCOUNTS_FILE, "r") as file:
        for line in file:
            if line.strip() == "":
                continue
            id, type, person_name, adress = line.strip().split(",")
            accounts.append(Account(
                id=int(id),
                type=type,
                person_name=person_name,
                adress=adress,
            ))
    return accounts

def save_all_accounts(accounts):
    with open(ACCOUNTS_FILE, "w") as file:
        for account in accounts:
            file.write(f"{account.id},{account.type},{account.person_name},{account.adress}\n")


if not os.path.exists("accounts.txt"):
        open("accounts.txt", "w").close()
# type hint for a list of accounts
accounts:list[Account] = read_accounts_from_file()

@app.post("/accounts/", status_code=201)
def create_account(account: Account):
    accounts = read_accounts_from_file()
    accounts.append(account)
    save_all_accounts(accounts)
    return {"message": "Account created successfully"}

@app.get("/accounts/")
def get_accounts():
    return read_accounts_from_file()

@app.get("/accounts/{account_id}")
def get_account(account_id: str):
    accounts = read_accounts_from_file()
    for account in accounts:
        if account.id == account_id:
            return account
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Account not found")

@app.delete("/accounts/{account_id}")
def delete_account(account_id: str):
    accounts = read_accounts_from_file()
    new_accounts = [account for account in accounts if account.id != account_id]
    if len(new_accounts) == len(accounts):
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Account not found")
    save_all_accounts(new_accounts)
    return {"message": "Account deleted successfully"}
