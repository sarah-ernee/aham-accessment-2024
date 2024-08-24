import os
import json
import logging

from fastapi import FastAPI, status, HTTPException
from typing import List
from dotenv import load_dotenv
from pathlib import Path

from pydantic import ValidationError

from app.definitions import FundDetails
import app.helper as helper

# Initialize environment variables
load_dotenv(dotenv_path=Path('app/.env'))
json_file_name = os.getenv("JSON_PATH", "temp_db.json")
FILE_DIR = Path.cwd() / json_file_name

if not FILE_DIR:
    raise ValueError("Failed to load JSON_PATH env var")

# Set logging config
logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s', filename='app.log', filemode='a')
logger = logging.getLogger(__name__)


app = FastAPI()

# ------------------------------------ API Endpoints ----------------------------------------- #

@app.get("/get-funds", status_code=status.HTTP_201_CREATED)
async def retrieve_all_funds() -> List[FundDetails]:
    '''
    Reads from JSON file to retrieve all funds.

    Returns: 
        - funds_list (list): a list of dictionaries containing fund details

    Sample return:
    [
        {
            "id": "fund001",
            "fund_name": "Global Equity Fund",
            "manager_name": "John Doe",
            "desc": "A diversified equity fund focusing on global markets.",
            "net_asset": 1500000.75,
            "created_at": "2024-08-22T14:30:00Z",
            "performance": 7.5
        }
    ]
    '''
    funds = helper.load_json(FILE_DIR)
    funds_list = []

    if len(funds) == 0:
        logger.warning("Fund database is currently empty")
        return []

    for fund in funds:
        try:
            # Explicit mapping of key-value pairs for better control
            dict = {
                "id": fund["id"],
                "fund_name": fund["fund_name"],
                "manager_name": fund["manager_name"],
                "desc": fund["desc"],
                "net_asset": fund["net_asset"],
                "created_at": fund["created_at"],
                "performance": fund["performance"]
            }

            fund_details = FundDetails(**dict)

        except ValidationError as e:
            logger.warning(f"Pydantic validation error with mapped fund object")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to retrieve all funds: {e}")
        
        try:
            funds_list.append(fund_details)
        
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to retrieve all funds: {e}")

    logger.info(f"Retrieved {len(funds_list)} number of funds from the system.")
    return funds_list

# need to make sure it's not the same name too?
@app.post("/create-fund")
async def create_fund(fund: FundDetails) -> None:
    '''
    Adds a new fund to the fund investment database.

    Args: 
        - fund (dict): a new fund object to append

    Sample request body:
        {
            "id": "fund001",
            "fund_name": "Global Equity Fund",
            "manager_name": "John Doe",
            "desc": "A diversified equity fund focusing on global markets.",
            "net_asset": 1500000.75,
            "created_at": "2024-08-22T14:30:00Z",
            "performance": 7.5
        }
    '''
    funds = helper.load_json(FILE_DIR)

    # Check if the fund is already in DB or not
    if any(f['id'] == fund.id for f in funds):
        logger.warning(f"Fund {fund.id} already exists in the system")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Fund was not created to avoid duplication conflict")

    try: 
        funds.append(fund.model_dump())
        helper.save_json(FILE_DIR, funds)
    
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create fund: {e}")
    
    logger.info(f"Fund created with id: {fund.id}")
    return {"message": "Successfully created new fund"}


@app.get("/get-one-fund/{id}")
async def retrieve_specific_fund(id: str) -> FundDetails:
    '''
    Reads from JSON file to retrieve fund given the specified fund ID.

    Args: 
        - id (str): fund ID identifier
    Returns: 
        - fund (dict): a dictionary containing fund details

    Sample return:
        {
            "id": "fund001",
            "fund_name": "Global Equity Fund",
            "manager_name": "John Doe",
            "desc": "A diversified equity fund focusing on global markets.",
            "net_asset": 1500000.75,
            "created_at": "2024-08-22T14:30:00Z",
            "performance": 7.5
        }
    '''
    funds = helper.load_json(FILE_DIR)
    specific_fund = None

    try:
        # Exit for loop once specific fund is found
        for fund in funds:
            if fund["id"] == id:
                specific_fund = fund 
                break
        
        # Prompt if fund does not exist in DB
        if specific_fund is None:
            logger.warning(f"Fund {id} was not found in the system")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to retrieve specific fund.")
    
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to retrieve specific fund: {e}")

    logger.info(f"Fund {id} successfully retrieved")
    return specific_fund


@app.patch("/update-fund/{id}")
async def update_fund_performance(id: str, performance: float) -> None:
    '''
    Updates specific fund performance percentage with given fund id.

    Args:
        - id (str): fund ID identifier
        - performance (float): fund performance value
    '''

    funds = helper.load_json(FILE_DIR)

    fund = None
    for f in funds:
        if f.get('id') == id:
            fund = f
            break

    # Check if fund is in DB or not
    if fund is None:
        logger.warning(f"Fund {id} was not found in the system")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to update fund performance.")
    
    # Check if passed in performance is a valid percentage
    if not 0 <= performance <= 100:
        logger.warning(f"Performance cannot be updated to an invalid value of {performance}%")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update fund performance.")
    
    try: 
        fund["performance"] = performance
        helper.save_json(FILE_DIR, funds)
    
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update fund: {e}")

    logger.info(f"Fund {id} performance updated  to {performance}%")
    return {"message" : "Successfully updated fund performance"}


@app.delete("/remove-fund/{id}")
async def delete_fund(id: str) -> None:
    '''
    Deletes fund from fund investment database given fund ID.
    Args:
        - id (str): fund ID identifier    
    '''

    funds = helper.load_json(FILE_DIR)

    fund = None
    for f in funds:
        if f.get('id') == id:
            fund = f
            break

    # Check if fund is in DB or not
    if fund is None:
        logger.warning(f"Fund {id} was not found in the system")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to delete fund")
    
    try:
        funds.remove(fund)
        helper.save_json(FILE_DIR, funds)

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete fund: {e}")

    logger.info(f"Fund {id} has been removed from the system")
    return {"message": "Successfully deleted fund"}