import re
import contractions
from nltk.corpus import stopwords
import en_core_web_sm

def textprep(input_str):
    str1 = contractions.fix(input_str)
    str2 = re.sub('[^a-zA-z0-9\s]','',str1)
    
    def lowerCase(input_str):
        input_str = input_str.lower()
        return input_str
    
    str3 = lowerCase(str2)
    
    sp = en_core_web_sm.load()
    stpw = set(stopwords.words('english'))
    
    def lemma(input_str):
        s = sp(input_str)
        
        input_list = []
        for word in s:
            w = word.lemma_
            input_list.append(w)
            
        output = ' '.join(word for word in input_list if word not in stpw)
        return output
    
    str4 = lemma(str3)
    return str4