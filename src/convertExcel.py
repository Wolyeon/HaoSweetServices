import pandas as pd
import re
import json

def cleanDF(df: pd.DataFrame) -> pd.DataFrame:
    labels = ["name", "pic", "sizes", "price", "tested", "finalized", "description", "Notes", "type"]
    df.columns = labels
    # We dont need the picture or notes as those are internal usage only
    df = df.drop(["pic", "Notes"], axis=1)
    # We want to drop the index numbers as they are just taking up space
    df = df.drop(0, axis=0)
    # We want to add in another column that will be used for resolving the image URL
    df["image"] = df["name"]
    # In the event some cells are not filled out we should fill them in.
    # This is not really ok but is fine since our data is small 
    df["description"].fillna("No Description", inplace=True)
    df["sizes"].fillna("No set sizes yet", inplace=True)
    df["price"].fillna("No price set yet", inplace=True)

    # In order to display the different sizes, we need to split the sizes from what
    # is shown on the excel sheet. We will use RE to split for back slashes (/) and word (or)
    df["sizes"] = df["sizes"].apply(lambda x: re.split(" / | or ", x))
    print(df["sizes"])

    # To ensure datatypes are consistent across multiple rows we will
    # cast the columns that can have varying types to a set type.
    df["price"] = df["price"].astype(str)
    df["tested"] = df["tested"].astype(bool)
    df["finalized"] = df["finalized"].astype(bool)
    return df                                                                       

def changeIndexToName(df: pd.DataFrame) -> pd.DataFrame:
    df.index = df["name"]
    return df


xcel = pd.ExcelFile("Menu.xlsx")
cakeDF = pd.read_excel("Menu.xlsx", "Cakes").assign(type="cake")
tartDF = pd.read_excel("Menu.xlsx", "Tarts").assign(type="tart")
otherDF = pd.read_excel("Menu.xlsx", "Other").assign(type="other")

cakeDF = cleanDF(cakeDF)
tartDF = cleanDF(tartDF)
otherDF = cleanDF(otherDF)

# Need to create a DF with the entire cake list as we will use
# this for grabbing cakes by their IDs instead of using a DB
totDF = pd.concat([cakeDF, tartDF, otherDF]).reset_index(drop=True)

# Using the index numbers we give each cake a unique ID number
totDF["productId"] = totDF.index.astype(str)
print(totDF.dtypes)
totDF.to_json("AllCakes.json", orient="index")
totDF.to_json("products.json", orient="records")

# We want to print out the json in each line as an individual json object
# so we orient by records.
totDF.loc[totDF["type"]=="cake"].to_json("cakeInfo.json", orient="records")
totDF.loc[totDF["type"]=="tart"].to_json("tartInfo.json", orient="records")
totDF.loc[totDF["type"]=="other"].to_json("otherInfo.json", orient="records")