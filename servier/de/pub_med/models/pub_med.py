from helpers.cleaning import transform_date, reject_tag, json_cleaner, default_cleaner
from helpers.alerts import rejections_alert
import yaml

from datetime import datetime
import pandas as pds

class PubMedData:
    """
    This class translates the business requirements and logic. 
    It aims to create a map of drugs and their links towards pubmed, clinical tests, journals.

    func : run_job() unwrap the full process 
    """

    # Deprecated
    dict_file_processors = {
        "clinical_trials" : ...,
        "drugs" : ...,
        "pubmed" : ...,
        
    }
    
    def __init__(self, **kwargs) -> None:
        """
        """

        self.path = '/'.join(__file__.split('/')[:-2])

        # Load Config File
        with open(f"{self.path}/config/main.yml", "r") as yaml_conf_file:
            self.conf = yaml.load(yaml_conf_file, Loader=yaml.FullLoader)

        
        self.today_str = datetime.now().strftime('%Y-%m-%d')

        pass

    def _processor__clinical_trials(self) -> pds.DataFrame:
        """
        """

        df_source = default_cleaner(pds.read_csv(f"{self.path}/{self.conf['PUBMED']['PATH']['SOURCEDIR']}/clinical_trials.csv", sep=","))
        
        col_list = df_source.columns.values

        for col in col_list:
            # print(col)
            if col == "date":
                df_source[col] = df_source[col].apply(transform_date).dt.strftime('%Y-%m-%d')
                print('end')

            df_source['rejected'] = df_source[col].apply(reject_tag)
            # print(df_source)
            # print(df_source.loc[df_source.rejected].filter(items=col_list))
            df_source.loc[df_source.rejected].filter(items=col_list).to_csv(f"{self.path}/{self.conf['PUBMED']['PATH']['REJECTIONDIR']}/{self.today_str}_clinical_trials_rejected.csv", mode='a', index=False, header=False)
            df_source = df_source.loc[df_source.rejected == False]
        
        return df_source

    def _processor__durgs(self) -> None:
        """
        """

        df_source = pds.read_csv(f"{self.path}/{self.conf['PUBMED']['PATH']['SOURCEDIR']}/drugs.csv", sep=",")
        col_list = df_source.columns.values

        for col in col_list:
            # print(col)
            df_source['rejected'] = df_source[col].apply(reject_tag)
            # print(df_source)
            # print(df_source.loc[df_source.rejected].filter(items=col_list))
            df_source.loc[df_source.rejected].filter(items=col_list).to_csv(f"{self.path}/{self.conf['PUBMED']['PATH']['REJECTIONDIR']}/{self.today_str}_drugs_rejected.csv", mode='a', index=False, header=False)
            df_source = df_source.loc[df_source.rejected == False]
    
        return df_source
    
    def _processor__pubmed(self, format='csv') -> None:
        """
        """

        import numpy as np

        # Extraction
        if format.lower() =='csv':
            df_source = pds.read_csv(f"{self.path}/{self.conf['PUBMED']['PATH']['SOURCEDIR']}/pubmed.csv", sep=",")
            # print(df_source.info())
        else:
            js_file = open(f"{self.path}/{self.conf['PUBMED']['PATH']['SOURCEDIR']}/pubmed.json", 'r')
            df_source = pds.read_json(json_cleaner(js_file.read()), orient='records')
            # df_source = pds.read_json("/Users/yserir/Personnel/Python_test_DE/servier/de/pub_med/data/source/pubmed.json")
            # print(df_source)
            # exit()
            # print("here")
            # print(df_source.dtypes)
            
        col_list = df_source.columns.values

        for col in col_list:
            # print(col)

            if col == "date":
                df_source[col] = df_source[col].apply(transform_date).dt.strftime('%Y-%m-%d')
                # print('end')

            df_source['rejected'] = df_source[col].apply(reject_tag)
            # print(df_source)
            # print(df_source.loc[df_source.rejected].filter(items=col_list))
            df_source.loc[df_source.rejected].filter(items=col_list).to_csv(f"{self.path}/{self.conf['PUBMED']['PATH']['REJECTIONDIR']}/{self.today_str}_pubmed_rejected.csv", mode='a', index=False, header=False)
            df_source = df_source.loc[df_source.rejected == False]

        return df_source

    

    def extract(self) -> dict:

        df_clinical_trials = self._processor__clinical_trials()
        print(df_clinical_trials)

        df_drugs = self._processor__durgs()

        df_csv = self._processor__pubmed(format='csv')
        df_json = self._processor__pubmed(format='json')
        df_pubmed = pds.concat([df_csv, df_json])


        return {
            'clinical_trials_dataframe' : df_clinical_trials,
            'pubmed_dataframe' : df_pubmed,
            'drugs_dataframe' : df_drugs
        }



    def transform(self, **kwargs) -> list:

        drugs_dict = kwargs['drugs_dataframe'].to_dict(orient='records')
        durgs_list = list()

        for drugs in drugs_dict:
            # print(drugs.keys())
            drugs['map'] = dict()
            papers = list()
            drug = drugs['drug'].lower()
            
            # print(drug)
            df_durg_in_ct =  kwargs['clinical_trials_dataframe'][kwargs['clinical_trials_dataframe'].apply(lambda i : drug in i['scientific_title'].lower(),  axis=1)]
            ct_dict = df_durg_in_ct.to_dict(orient='records')
            drugs['map']['clinical_trials'] = [{'title' : ct['scientific_title'], 'date' : ct['date']} for ct in ct_dict]
            papers = [{'title' : ct['journal'],'date': ct['date']} for ct in ct_dict]

            df_durg_in_pubmed =  kwargs['pubmed_dataframe'][kwargs['pubmed_dataframe'].apply(lambda i : drug in i['title'].lower(),  axis=1)]
            ct_dict = df_durg_in_pubmed.to_dict(orient='records')
            drugs['map']['pubmed'] = [{'title' : ct['title'], 'date' : ct['date']} for ct in ct_dict]
            papers += [{'title' : ct['journal'],'date': ct['date']} for ct in ct_dict]

            # Check if the paper is unique
            df_papers = pds.DataFrame.from_dict(papers)
            drugs['map']['journal'] = df_papers.drop_duplicates().to_dict(orient='records', )

            durgs_list.append(drugs)
            # print(drugs)
            # print(papers)
            # print('*' * 99)
        return durgs_list

    def load(self, durgs : list) -> None:
        import json 

        with open(f"{self.path}/{self.conf['PUBMED']['PATH']['DESTDIR']}/graph_drugs.json", 'w') as js_file:
            json.dump(durgs, js_file, indent=4, ensure_ascii=False)
        

    def run_job(self, alert : bool):

        dataframes_extracted = self.extract()
        drugs_graph_list = self.transform(**dataframes_extracted)
        self.load(drugs_graph_list)

        if alert:
            rejections_alert(f"{self.path}/{self.conf['PUBMED']['PATH']['REJECTIONDIR']}")
        
        
        pass