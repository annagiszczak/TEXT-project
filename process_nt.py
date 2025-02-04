import pandas as pd

df = pd.read_csv("data/OGNT_full.csv",
                 sep="\t",
                 dtype=str,
                 usecols=("〔Book｜Chapter｜Verse〕",
                          "〔BDAGentry｜EDNTentry｜MounceEntry｜GoodrickKohlenbergerNumbers｜LN-LouwNidaNumbers〕", 
                          "〔TBESG｜IT｜LT｜ST｜Español〕",
                          )
                )

book_names = ["mt", "mk", "lk", "j", "acts", "rom", "1kor", "2kor", "gal", "eph", "phi", "col", "1tes", "2tes", "1tym", "2tym", "tit", "fil", "heb", "jam", "1pet", "2pet", "1j", "2j", "3j", "jd", "rev"]

author_dict = {
    "mt": "matthew", 
    "mk": "mark", 
    "lk": "luke", 
    "j": "john", 
    "acts": "luke", 
    "rom": "paul", 
    "1kor": "paul",
    "2kor": "paul", 
    "gal": "paul", 
    "eph": "paul", 
    "phi": "paul", 
    "col": "paul", 
    "1tes": "paul", 
    "2tes": "paul", 
    "1tym": "paul", 
    "2tym": "paul", 
    "tit": "paul", 
    "fil": "paul", 
    "heb": "unknown", 
    "jam": "james", 
    "1pet": "peter", 
    "2pet": "peter", 
    "1j": "john", 
    "2j": "john", 
    "3j": "john", 
    "jd": "jude", 
    "rev": "john"
}

# decode address
addresses = df.iloc[:,0].apply(lambda x: x.strip('〔〕').split('｜'))
df["book"] = [list(author_dict.keys())[int(a[0]) - 40] for a in addresses] # book is coded with book number starting with 40
df["chapter"] = [int(a[1]) for a in addresses]
df["verse"] = [int(a[2]) for a in addresses]

# decode word
df["token"] = df.iloc[:,1].apply(lambda x: x.strip('〔〕').split('｜')[0])

# decode translation
df["trans"] = df.iloc[:,2].apply(lambda x: x.strip('〔〕').split('｜')[0])

# authorship
df["author"] = df["book"].apply(lambda x: author_dict[x])

df.drop("〔Book｜Chapter｜Verse〕", axis=1, inplace=True)
df.drop("〔BDAGentry｜EDNTentry｜MounceEntry｜GoodrickKohlenbergerNumbers｜LN-LouwNidaNumbers〕", axis=1, inplace=True)
df.drop("〔TBESG｜IT｜LT｜ST｜Español〕", axis=1, inplace=True)

df.to_csv("data/OGNT_processed.csv")