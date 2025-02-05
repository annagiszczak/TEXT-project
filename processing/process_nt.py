import pandas as pd

df = pd.read_csv("../data/OGNT_full.csv",
                 sep="\t",
                 dtype=str,
                 usecols=("〔Book｜Chapter｜Verse〕",
                          "〔OGNTk｜OGNTu｜OGNTa｜lexeme｜rmac｜sn〕",
                        #   "〔BDAGentry｜EDNTentry｜MounceEntry｜GoodrickKohlenbergerNumbers｜LN-LouwNidaNumbers〕", 
                          "〔TBESG｜IT｜LT｜ST｜Español〕",
                          )
                )

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
addresses = df["〔Book｜Chapter｜Verse〕"].apply(lambda x: x.strip('〔〕').split('｜'))
df["book"] = [list(author_dict.keys())[int(a[0]) - 40] for a in addresses] # book is coded with book number starting with 40
df["chapter"] = [int(a[1]) for a in addresses]
df["verse"] = [int(a[2]) for a in addresses]

# decode word
# df["token"] = df["〔BDAGentry｜EDNTentry｜MounceEntry｜GoodrickKohlenbergerNumbers｜LN-LouwNidaNumbers〕"].apply(lambda x: x.strip('〔〕').split('｜')[0])
df["word"] = df["〔OGNTk｜OGNTu｜OGNTa｜lexeme｜rmac｜sn〕"].apply(lambda x: x.strip('〔〕').split('｜')[1])

# decode lemma
df["lemma"] = df["〔OGNTk｜OGNTu｜OGNTa｜lexeme｜rmac｜sn〕"].apply(lambda x: x.strip('〔〕').split('｜')[3])

# decode translation
df["trans"] = df["〔TBESG｜IT｜LT｜ST｜Español〕"].apply(lambda x: x.strip('〔〕').split('｜')[0])

# authorship
df["author"] = df["book"].apply(lambda x: author_dict[x])

df.drop("〔Book｜Chapter｜Verse〕", axis=1, inplace=True)
df.drop("〔OGNTk｜OGNTu｜OGNTa｜lexeme｜rmac｜sn〕", axis=1, inplace=True)
# df.drop("〔BDAGentry｜EDNTentry｜MounceEntry｜GoodrickKohlenbergerNumbers｜LN-LouwNidaNumbers〕", axis=1, inplace=True)
df.drop("〔TBESG｜IT｜LT｜ST｜Español〕", axis=1, inplace=True)

df.to_csv("../data/OGNT_processed.csv")