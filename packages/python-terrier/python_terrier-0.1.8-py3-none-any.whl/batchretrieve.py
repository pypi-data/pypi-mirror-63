from jnius import autoclass, cast
from utils import *
import pandas as pd
import numpy as np
from pyterrier import properties as props

class BatchRetrieve:
    default_controls={
        "terrierql": "on",
        "parsecontrols": "on",
        "parseql": "on",
        "applypipeline": "on",
        "localmatching": "on",
        "filters": "on",
        "decorate":"on",
        "wmodel": "DPH",
    }

    default_properties={
        "querying.processes":"terrierql:TerrierQLParser,parsecontrols:TerrierQLToControls,parseql:TerrierQLToMatchingQueryTerms,matchopql:MatchingOpQLParser,applypipeline:ApplyTermPipeline,localmatching:LocalManager$ApplyLocalMatching,qe:QueryExpansion,labels:org.terrier.learning.LabelDecorator,filters:LocalManager$PostFilterProcess",
        "querying.postfilters": "decorate:SimpleDecorate,site:SiteFilter,scope:Scope",
        "querying.default.controls": "wmodel:DPH,parsecontrols:on,parseql:on,applypipeline:on,terrierql:on,localmatching:on,filters:on,decorate:on",
        "querying.allowed.controls": "scope,qe,qemodel,start,end,site,scope",
        "termpipelines": "Stopwords,PorterStemmer"
    }

    def __init__(self, indexPath, controls=None, properties=None):
        JIR = autoclass('org.terrier.querying.IndexRef')
        indexRef = JIR.of(indexPath)

        self.IndexRef=indexRef
        self.appSetup = autoclass('org.terrier.utility.ApplicationSetup')

        self.properties=self.default_properties.copy()
        if type(properties)==type({}):
            for key,value in properties.items():
                self.properties[key]=value

        for key,value in self.properties.items():
            props.put(key,value)
        self.appSetup.bootstrapInitialisation(props)

        self.controls=self.default_controls.copy()
        if type(controls)==type({}):
            for key,value in controls.items():
                self.controls[key]=value

        MF = autoclass('org.terrier.querying.ManagerFactory')
        self.ManagerFactory = MF._from_(indexRef)

    def transform(self,queries):
        results=[]
        queries=Utils.form_dataframe(queries)
        for index,row in queries.iterrows():
            rank = 0
            srq = self.ManagerFactory.newSearchRequest(row['qid'],row['query'])
            for control,value in self.controls.items():
                srq.setControl(control,value)
            self.ManagerFactory.runSearchRequest(srq)
            result=srq.getResults()
            for item in result:
                res = [row['qid'],item.getMetadata("docno"),rank,item.getScore()]
                rank += 1
                # res = [queries.iloc[index]['qid'],item.getMetadata("docno"),item.getScore()]
                results.append(res)
        res_dt=pd.DataFrame(results,columns=['qid','docno','rank','score'])
        return res_dt

    def saveResult(self, result, path):
        res_copy = result.copy()
        res_copy.insert(1, "Q0", "Q0")
        res_copy.insert(5, "wmodel", self.controls["wmodel"])
        res_copy.to_csv(path, sep=" ", header=False, index=False)

    def setControls(self, controls):
        for key, value in controls.items():
            self.controls[key]=value

    def setControl(self, control,value):
        self.controls[control]=value


class FeaturesBatchRetrieve(BatchRetrieve):
    default_controls = BatchRetrieve.default_controls
    default_controls["matching"] = "FatFeaturedScoringMatching,org.terrier.matching.daat.FatFull"
    default_properties = BatchRetrieve.default_properties
    def __init__(self, indexPath, features, controls=None, properties=None):
        props.put("fat.featured.scoring.matching.features",";".join(features))
        super().__init__(indexPath,controls=controls,properties=properties)

    def transform(self,topics):
        results=[]
        queries=Utils.form_dataframe(topics)
        for index,row in queries.iterrows():
            srq = self.ManagerFactory.newSearchRequest(row['qid'],row['query'])
            for control,value in self.controls.items():
                srq.setControl(control,value)
            self.ManagerFactory.runSearchRequest(srq)
            srq=cast('org.terrier.querying.Request',srq)
            fres=cast('org.terrier.learning.FeaturedResultSet', srq.getResultSet())
            feats = fres.getFeatureNames()
            for i in range(fres.getResultSize()):
                elem=[]
                elem.append(row['qid'])
                elem.append(fres.getMetaItems("docno")[i])
                elem.append(fres.getScores()[i])
                feats_array = np.array([])
                for feat in feats:
                    feats_array = np.append(feats_array, fres.getFeatureScores(feat)[i])
                elem.append(feats_array)
                results.append(elem)
        res_dt=pd.DataFrame(results, columns=["qid", "docno", "score", "features"])
        return res_dt
