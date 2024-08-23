import os
import json
import logging

from fastapi import FastAPI, status, HTTPException
from typing import List
from dotenv import load_dotenv
from pathlib import Path

from app.definitions import FundDetails
import app.helper as helper

# Initialize environment variables
load_dotenv()
FILE_DIR = os.getenv("JSON_PATH")

# Set logging config
logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s', filename='app.log', filemode='a')
logger = logging.getLogger(__name__)


app = FastAPI()

# ------------------------------------ API Endpoints ----------------------------------------- #

@app.get("/funds", status_code=status.HTTP_201_CREATED)
async def retrieve_all_funds() -> List[FundDetails]:
    '''
    Reads from JSON file to retrieve all funds.

    Returns: 
        - funds_list (list): a list of dictionaries containing fund details
    '''
    funds = helper.load_json(FILE_DIR)
    funds_list = []

    for fund in funds.values():
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

        except (KeyError, ValueError) as e:
            logger.warning(f"Fund mapping does not match Pydantic base model")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail=f"Error in dict key-value pairs: {e}")
        
        try:
            funds_list.append(fund_details)
        
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail=f"Failed to retrieve all funds: {e}")

    logger.info(f"Retrieved {len(funds_list)} number of funds from the system.")
    return funds_list


@app.post("/funds")
async def create_fund(fund: FundDetails) -> None:
    '''
    Adds a new fund to the fund investment database.

    Args: 
        - fund (dict): a new fund object to append
    '''
    funds = helper.load_json(FILE_DIR)

    if fund["id"] in funds:
        logger.warning(f"Fund {fund.id} already exists in the system")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Fund was not created to avoid duplication conflict")
    
    try: 
        funds[fund["id"]] = fund.model_dump()

        with open(Path(FILE_DIR), "w") as f:
            json.dump(funds, f, default=str)
    
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail=f"Failed to create fund: {e}")
    
    logger.info(f"Fund created with id: {fund["id"]}")
    return {"message:" "Successfully created new fund"}


@app.get("/funds/{id}")
async def retrieve_specific_fund(id: str) -> FundDetails:
    '''
    Reads from JSON file to retrieve fund given the specified fund ID.

    Args: 
        - id (str): fund ID identifier
    Returns: 
        - fund (dict): a dictionary containing fund details
    '''
    funds = helper.load_json(FILE_DIR)

    try:
        fund = funds[id]
    except KeyError:
        logger.warning(f"Fund {id} was not found in the system")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Failed to retrieve specific fund.")
    
    specific_fund = {
        "id": fund["id"],
        "fund_name": fund["fund_name"],
        "manager_name": fund["manager_name"],
        "desc": fund["desc"],
        "net_asset": fund["net_asset"],
        "created_at": fund["created_at"],
        "performance": fund["performance"]
    }

    logger.info(f"Fund {id} successfully retrieved")
    return specific_fund


@app.patch("/funds/{id}")
async def update_fund_performance(id: str, performance: float) -> None:
    '''
    Updates specific fund performance percentage with given fund id.

    Args:
        - id (str): fund ID identifier
        - performance (float): fund performance value
    '''

    funds = helper.load_json(FILE_DIR)

    if id not in funds:
        logger.warning(f"Fund {id} was not found in the system")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Failed to update fund performance.")
    
    if not 0 <= performance <= 100:
        logger.warning(f"Performance cannot be updated to an invalid value of {performance}%")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Failed to update fund performance.")
    
    try: 
        funds[id]["performance"] = performance
        with open(Path(FILE_DIR), "w") as f:
            json.dump(funds, f, default=str)
    
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail=f"Failed to update fund: {e}")

    logger.info(f"Fund {id} performance updated  to {performance}%")
    return {"message" : "Successfully updated fund performance"}


@app.delete("/funds/{id}")
async def delete_fund(id: str) -> None:
    '''
    Deletes fund from fund investment database given fund ID.
    Args:
        - id (str): fund ID identifier    
    '''

    funds = helper.load_json(FILE_DIR)

    if id not in funds:
        logger.warning(f"Fund {id} was not found in the system")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Failed to delete fund.")
    
    try:
        del funds[id]
        with open(Path(FILE_DIR), "w") as f:
            json.dump(funds, f, default=str)

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail=f"Failed to delete fund: {e}")

    logger.info(f"Fund {id} has been removed from the system")
    return {"message": "Successfully deleted fund"}