import pandas as pd

def cleanDF(df: pd.DataFrame) -> pd.DataFrame:
    labels = ["name", "pic", "sizes", "price", "tested", "finalized", "description", "Notes"]
    df.columns = labels
    df = df.drop(["pic", "Notes"], axis=1)
    df = df.drop(0, axis=0)
    # In the event some cells are not filled out we should fill them in.
    df["description"].fillna("No Description", inplace=True)
    df["sizes"].fillna("No set sizes yet", inplace=True)
    df["price"].fillna("No price set yet", inplace=True)
    return df                                                                       

xcel = pd.ExcelFile("Menu.xlsx")
cakeDF = pd.read_excel("Menu.xlsx", "Cakes")
tartDF = pd.read_excel("Menu.xlsx", "Tarts")
otherDF = pd.read_excel("Menu.xlsx", "Other")

cakeDF = cleanDF(cakeDF)
tartDF = cleanDF(tartDF)
otherDF = cleanDF(otherDF)

print(cakeDF)

cakeDF.to_json("cakeInfo.json", orient="records")