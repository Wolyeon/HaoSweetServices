import pandas as pd

def cleanDF(df: pd.DataFrame) -> pd.DataFrame:
    labels = ["name", "pic", "sizes", "price", "tested", "finalized", "description", "Notes"]
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
    df["tested"] = df["tested"].astype(bool)
    df["finalized"] = df["finalized"].astype(bool)
    print(df.dtypes)
    return df                                                                       

def changeIndexToName(df: pd.DataFrame) -> pd.DataFrame:
    df.index = df["name"]
    return df


xcel = pd.ExcelFile("Menu.xlsx")
cakeDF = pd.read_excel("Menu.xlsx", "Cakes")
tartDF = pd.read_excel("Menu.xlsx", "Tarts")
otherDF = pd.read_excel("Menu.xlsx", "Other")

cakeDF = cleanDF(cakeDF)
tartDF = cleanDF(tartDF)
otherDF = cleanDF(otherDF)

indCakeDF = changeIndexToName(cakeDF)
indTartDF = changeIndexToName(tartDF)
inOtherDF = changeIndexToName(otherDF)

totDF = pd.concat([indCakeDF, indTartDF, inOtherDF])
totDF.to_json("AllCakes.json", orient="index")

# We want to print out the json in each line as an individual object
# so we orient by records.
cakeDF.to_json("cakeInfo.json", orient="records")
tartDF.to_json("tartInfo.json", orient="records")
otherDF.to_json("otherInfo.json", orient="records")