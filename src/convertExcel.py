import pandas as pd

def cleanDF(df: pd.DataFrame) -> pd.DataFrame:
    labels = ["Name", "pic", "Available Sizes", "Price", "Tested", "Finalized", "Description", "Notes"]
    df.columns = labels
    df = df.drop(["pic", "Notes"], axis=1)
    df = df.drop(0, axis=0)
    return df

xcel = pd.ExcelFile("Menu.xlsx")
cakeDF = pd.read_excel("Menu.xlsx", "Cakes")
tartDF = pd.read_excel("Menu.xlsx", "Tarts")
otherDF = pd.read_excel("Menu.xlsx", "Other")

cakeDF = cleanDF(cakeDF)
tartDF = cleanDF(tartDF)
otherDF = cleanDF(otherDF)

print(cakeDF)
print(tartDF)
print(otherDF)

cakeDF.to_json("cakeData.json")