from models.pub_med import PubMedData

import pandas as pds

print("Hello Let\'s Start")
d = PubMedData()
#01.
# ndata = d.processor__clinical_trials()
#02.
# ndata = d._processor__durgs()
# print(ndata.to_dict(orient='records'))

#03.1
# ndata = d.processor__pubmed(format='csv')
#03.2
# ndata = d.processor__pubmed(format='json')

# print(ndata.shape)
# print(ndata.info())
# print(ndata.head(20))
# d.extract()

d.run_job(alert=True)

