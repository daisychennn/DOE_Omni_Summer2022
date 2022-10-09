# get appropriate libraries 
import xml.dom.minidom
import numpy as np
import pandas as pd
import os
import nltk
#nltk.download('stopwords','punkt','wordnet','omw-1.4')
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import MWETokenizer
snowball_stemmer = SnowballStemmer('english')
wordnet_lemmatizer = WordNetLemmatizer()
english_stopwords = stopwords.words("english")
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator


class ReadXML:  
    def __init__(self, path, f_ns, saved_name, yearinput, keywordinput, keywordexclude):
        self.df_all =self.readxml(path, f_ns, yearinput, keywordinput)
        self.pipelines(path, f_ns, self.df_all, saved_name, keywordexclude)


    def readxml(self,path,file_names,yearinput,keywordinput):
        i = 0
        df = pd.DataFrame()
        ndf = pd.DataFrame()
        final_df = pd.DataFrame()
        outpath = path+r'/output/' 
        if not os.path.exists(outpath):
            os.makedirs(outpath)
        for fn in file_names:
            dom = xml.dom.minidom.parse(path+'/xmls/' + fn)
            root = dom.documentElement
            records = root.getElementsByTagName('record')
            for record in records:
                # get info from xml to put into df
                try:
                    title = record.getElementsByTagName('title')[0].childNodes[0].data
                    df.loc[i, 'title'] = title
                except:
                    pass
                try:
                    year = int(record.getElementsByTagName('year')[0].childNodes[0].data)                    
                    df.loc[i, 'year'] = year
                except:
                    pass
                try:
                    keywords = ", ".join([a.childNodes[0].nodeValue for node in record.getElementsByTagName('keywords') for a in node.getElementsByTagName('keyword')])
                    df.loc[i, 'keywords'] = keywords
                except:
                    pass
                try:
                    abstract = record.getElementsByTagName('abstract')[0].childNodes[0].data
                    df.loc[i, 'abstract'] = abstract
                except:
                    pass
                i += 1
                
            # year filter 
            if yearinput == []:
                pass
            else:   
                for x in yearinput:
                    x=int(x)
                    ndf = ndf.append(df[df['year']==x]) 
                df = ndf
            # keyword filter 
            if keywordinput == []:
                pass
            else:
                for x in keywordinput:
                    final_df = final_df.append(df[df['title'].str.contains(x,na=False)])
                    final_df = final_df.append(df[df['keywords'].str.contains(x,na=False)])
                    final_df = final_df.append(df[df['abstract'].str.contains(x,na=False)])
                    final_df = final_df.drop_duplicates()
                df = final_df
        return df

    def pipelines(self,path, f_n, df, saved_name, keywordexclude):
        f_n = f_n[0].split('.')[0]
        df = df.fillna('')      
        
        # read ban_list
        # to exclude from word cloud
        try:
            with open(path + '/ban_list.txt', 'r') as f:
                b_list = f.readlines()[0].split(',')
        except:
            pass

        full_text = ' '.join(df['title'].values) + ' '.join(df['keywords'].values) + ' '.join(df['abstract'].values)        
        # multi-word tokenizer combines words into a single token
        tokenizer = MWETokenizer(
            [('ionic', 'liquid'), ('post', 'combustion'), ('activated', 'carbon'), ('ca', 'looping'),
             ('pre', 'combustion'), ('direct', 'air', 'capture'), ('renewable', 'thermal'),
             ('membrane', 'vacuum'), ('bipolar', 'membrane', 'electrodialysis'),
             ('calcium', 'looping'), ('chemical', 'looping'), ('electrical', 'swing'),
             ('electrical', 'regeneration'),
             ('temperature', 'swing'), ('pressure', 'swing'), ('ph', 'swing'), ('vacuum', 'swing'),
             ('oxy', 'fuel'), ('membrane', 'contactor'), ('hydrogen', 'production'), ('hollow', 'fiber'),
             ('co2', 'sequestration'), ('metal', 'organic', 'frameworks'), ('metal', 'organic', 'framework'),
             ('energy', 'efficiency'), ('energy', 'consumption'), ('aqueous', 'ammonia'),
             ('vacuum', 'swing', 'adsorption'),
             ('temperature', 'swing', 'adsorption')], separator='-')
        
        # sort through words
        value = nltk.sent_tokenize(full_text)
        new = []
        exclusions = [',', '(', ')', ':', ' ', '\'', '\'\'', '``', ' ', '+/ ', '\'s',
                    '`','“','”','.','+/','+','[',']','%','$','&','=','i.e.','<','>']
        exclusions += keywordexclude
        for i in value:
            words = tokenizer.tokenize(nltk.word_tokenize(text=i))
            for wo in words:
                wo = wordnet_lemmatizer.lemmatize(wo).lower()
                wo = wo.replace('-', ' ')
                if wo in english_stopwords:
                    continue
                try:
                    if wo in b_list:
                        continue
                except:
                    pass
                if wo in exclusions:
                    continue
                new.append(wo)
        s_full = self.sort_dict(new, sort=False)
        s_full2 = sorted(s_full.items(), key=lambda item: item[1], reverse=True)
    
        # create dataframe with words and their counts
        df2 = pd.DataFrame().from_dict(s_full2)
        
        # make bar graph for frequencies
        df2.columns = df2.columns.map(str)
        df2.columns = ['Keyword', 'Frequency']
        fig = df2.iloc[1:51].plot(kind='bar', x='Keyword', y='Frequency', ylabel='Frequency', 
                                  figsize=(8,3), legend=False).get_figure()
        fig.savefig(path+"/output/"+saved_name+"-frequencies", bbox_inches='tight')
        plt.close(fig)
        
        # print first 50 words
        j = 0
        for key, value in s_full2:
            if j <= 50:
                #print(key, ':', value)
                j += 1
            else:
                break
                
        # save dict into file
        self.write_dict(path+r"/output/"+saved_name, s_full2)

        # generate wordcloud and save to files
        del s_full['total']
        self.gene_wc(s_full, path+"/output/"+saved_name+"-word-cloud")
        
        # generate csv and save
        self.output_csv(df,path+r"/output/" +saved_name)
        

    @staticmethod
    def gene_wc(dt, name):
        wc = WordCloud(
            background_color="white",
            max_words=50,
            max_font_size=100,
            random_state=42,
            width=420, height=320, margin=1,
        )
        wc.fit_words(dt)
        plt.figure()
        plt.imshow(wc)
        plt.axis("off")
        wc.to_file('%s.png' % name )
        #plt.show()
        plt.close()

    @staticmethod
    def sort_dict(li, sort=True):
        d = {}
        total_number = 0
        for word in li:
            d[word] = d.get(word, 0) + 1
            total_number += 1
        d['total'] = total_number
        if sort:
            d = sorted(d.items(), key=lambda item: item[1], reverse=True)
        return d

    @staticmethod
    def write_dict(name, dt):
        with open('%s.txt' % name, 'w', encoding="utf-8") as file:
            for kw in dt:
                file.write(str(kw[0]) + ':' + str(kw[1]) + '\n')
    
    #save search as csv file 
    @staticmethod
    def output_csv(df, name):
        df.to_csv('%s.csv' % name) 


if __name__ == '__main__':
    y_li = ['plastic_or_polymer_highly_cited.xml']
    path = r'C:\Users\aysha\Documents\Work\MLEF_2022\plastic_or_polymer_allfields'
    saved_name = 'test'
    keywordinput = ['']
    keywordexclude = ['material']
    yearinput = ['2018']
    RD = ReadXML(path, y_li, saved_name, yearinput, keywordinput, keywordexclude)