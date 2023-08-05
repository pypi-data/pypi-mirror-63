# Pydval
Python Data Validator By R&amp;D ICWR
## Example Code
```python
print("""
#########################
# Example Code - pydval #
#########################
""")

import pydval

key_word={"After","taking","time","away","to","focus","on","general","relativity","Einstein","returned","to","July","1916"}
data_input=[
        "After taking time away to focus on general relativity, Einstein returned to the quantum theory of light in July 1916",
        "Einstein His efforts culminated in three papers, two in 1916 and the most prominent one in 1917",
        "It had been 16 years since Einstein Planck’s original theory"
    ]

print("[*] Multi Matching")
result=pydval.validator().multi_matching(key_word,data_input)
i=0
for x in result:
    i=i+1
    print("\t[*] Total Valid Answer From Number %s Is %s"%(i,len(x[i])))

single_data1="After taking time away to focus on general relativity, Einstein returned to the quantum theory of light in July 1916"
single_data2="Einstein His efforts culminated in three papers, two in 1916 and the most prominent one in 1917"
single_data3="It had been 16 years since Einstein Planck’s original theory"

print("[*] Single Matching")
print("\t[*] Total Valid From Answer %s"%(len(pydval.validator().matching(key_word,single_data1))))
print("\t[*] Total Valid From Answer %s"%(len(pydval.validator().matching(key_word,single_data2))))
print("\t[*] Total Valid From Answer %s"%(len(pydval.validator().matching(key_word,single_data3))))
```
