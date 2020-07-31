
#from flask_wtf import FlaskForm
#from wtforms import StringField
#from wtforms.validators import DataRequired
#from flask_bootstrap import Bootstrap
from flask import Flask, request, render_template,redirect
from tensorflow.python.keras.preprocessing.text import Tokenizer
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import pickle
from keras.models import Model, Sequential
import re
import tensorflow as tf
from keras.layers import Dense, LSTM, Flatten, Embedding, Dropout , Activation, GRU, Flatten, Input, Bidirectional, GlobalMaxPool1D, Convolution1D, TimeDistributed, Bidirectional
from keras.layers.embeddings import Embedding
#from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.feature_extraction.text import TfidfTransformer
#from wtforms.validators import DataRequired
import pandas as pd
from os.path import join
#from jpype import JClass, JString, getDefaultJVMPath, shutdownJVM, startJVM,java

'''
ZEMBEREK_PATH: str = join('..', '..', 'bin', '/home/busra/İndirilenler/zemberek-full.jar')
startJVM(
        getDefaultJVMPath(),
        '-ea',
        f'-Djava.class.path={ZEMBEREK_PATH}',
        convertStrings=False
    )
with open('templates/stopwords-tr.txt', 'r') as f:
    myList = [line.strip() for line in f]

tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words=myList)

'''

#app = Flask(__name__)
#Bootstrap(app)
#app.config['SECRET_KEY'] = "DontTellAnyone"

'''
class SearchForm(FlaskForm):
    name = StringField('query', validators=[DataRequired()])
'''






embed_size = 128
model = Sequential()
model.add(Embedding(15000, embed_size))
model.add(Bidirectional(LSTM(64, return_sequences = True)))
model.add(Bidirectional(LSTM(32, return_sequences = True)))
model.add(GlobalMaxPool1D())
model.add(Dense(1, activation="sigmoid"))

def check_1(text):#mı mi için model ile alına inputu düzeltcek
    with open('/home/ylmz/YlmzWorkSpace/fixy/ki_corrector/pre_trained_weights/tokenizer_ki.pickle', 'rb') as handle:
        turkish_tokenizer = pickle.load(handle)
    model.load_weights('/home/ylmz/YlmzWorkSpace/fixy/ki_corrector/pre_trained_weights/Model_ki.h5')
    tokens = turkish_tokenizer.texts_to_sequences(text)
    tokens_pad = pad_sequences(tokens, maxlen=7)
    result = model.predict(tokens_pad)
    print("dd")
    return result

def check_2(text):#de da için model ile alına inputu düzeltcek
    with open('fixy/pre_trained_weights/tokenizer_deda.pickle', 'rb') as handle:
        turkish_tokenizer = pickle.load(handle)
    model.load_weights('fixy/pre_trained_weights/Model_deda.h5')
    
    arr = text.split()

    for i in range(len(arr)):
        tmp = arr[i]
        last2 = arr[i][-2:]
        if(last2 == "de" or last2 == "da"):
            print(i)
            arr[i] = arr[i][:-2] + " x "
            changed = ' '.join(arr[0:])
            print(changed)
            tokens = turkish_tokenizer.texts_to_sequences(changed)
            tokens_pad = pad_sequences(tokens, maxlen=7)
            print(tokens)
            result = model.predict(tokens_pad)
            if(result[0][0]>0.5):
                
    
    
    
    

    
    print("dd")
    return str(result[0])

def check_3(text):#ki için model ile alına inputu düzeltcek
    #işlemler
    return text

print(check_2("ben de seninle geleceğim"))
'''
def sentiment(text):
    negative = 0
    positive = 0
    neutral = 0
    texts = text.split(".")
    max_tokens = 59
    # tokenizer'ı yükle
    with open('templates/turkish_tokenizer_hack.pickle', 'rb') as handle:
        turkish_tokenizer = pickle.load(handle)
    model = load_model('templates/hack_Model.h5')
    tokens = turkish_tokenizer.texts_to_sequences(texts)
    tokens_pad = pad_sequences(tokens, maxlen=max_tokens)
    for i in model.predict(tokens_pad):
        if i < 0.3:
           negative = negative + 1
        elif i == 0.3:
           neutral = neutral + 1
        else:
           positive = positive + 1

    if max(negative,neutral,positive)==negative:
        sentiment = "Negatif"
    elif max(negative,neutral,positive)==positive:
        sentiment = "Pozitif"
    else:
        sentiment = "Nötr"

    return "%" + str(100*max(negative,neutral,positive)/(negative+neutral+positive)) + " " + sentiment

def emotion(text):
    duygu = [ ]
    corpus = [text]
    loaded_model = pickle.load(open("templates/emotion_model.pickle", 'rb'))
    df = pd.read_csv('templates/KarışıkDuygular.csv')
    tfidf.fit_transform(df.Entry).toarray()
    features = tfidf.transform(corpus).toarray()
    result = loaded_model.predict(features)
    for i in result:
        if i == "Happy":
            duygu.append("Sevinçli, Umutlu")
        elif i =="Fear":
            duygu.append("Korkulu, Endişeli")
        elif i == "Anger":
            duygu.append("Öfkeli, Sinirli, Kızgın")
        elif i == "Sadness":
            duygu.append("Üzgün, Kederli, Dramatik")
        elif i == "Surprise":
            duygu.append("Şaşırmış, Şokta, Beklenmedik")
        elif i == "Disgust":
            duygu.append("İğrenmiş, Tiksinmiş, Bıkkın, Yılgın, Çaresiz, Üzgün")
    return duygu

def formal(text):
    formal = 0
    informal = 0
    texts = text.split(".")
    max_tokens = 59
    # load tokenizer
    with open('templates/tokenizer_FormalInformal.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    model = load_model('templates/MODEL_FORMAL.h5')
    tokens = tokenizer.texts_to_sequences(texts)
    tokens_pad = pad_sequences(tokens, maxlen=max_tokens)
    for i in model.predict(tokens_pad):
        if i < 0.3:
            informal = informal + 1
        else:
            formal = formal + 1

    if max(formal,informal) == informal:
        fr = "Informal"
        #fix = toFormal(text)
    else:
        fr = "Formal"
        #fix = ""
    return "%" + str(100 * max(formal,informal) / (formal + informal)) + " " + fr


def rule_based_corrector(text):

    paragraph = []
    Result = " "

    TurkishMorphology: JClass = JClass('zemberek.morphology.TurkishMorphology')
    TurkishSentenceNormalizer: JClass = JClass(
        'zemberek.normalization.TurkishSentenceNormalizer'
    )


    Paths: JClass = JClass('java.nio.file.Paths')

    for i, word in enumerate([text]):
        paragraph.append(word)

    normalizer = TurkishSentenceNormalizer(
        TurkishMorphology.createWithDefaults(),
        Paths.get(
            join('..', '..', 'data',
                 '/home/busra/PycharmProjects/Piton/myenv/Zemberek-Python-Examples-master/examples/normalization')
        ),
        Paths.get(
            join('..', '..', 'data', 'lm', '/home/busra/PycharmProjects/Piton/myenv/lm.2gram.slm')
        )
    )

    for i, example in enumerate(paragraph):
        Result = Result + str(normalizer.normalize(JString(example))).capitalize() + " "

    return Result
    #shutdownJVM()



def toFormal(text):

    formal = " "

    TurkishMorphology: JClass = JClass('zemberek.morphology.TurkishMorphology')
    RootLexicon: JClass = JClass('zemberek.morphology.lexicon.RootLexicon')
    InformalAnalysisConverter: JClass = JClass(
        'zemberek.morphology.analysis.InformalAnalysisConverter'
    )

    morphology: TurkishMorphology = (
        TurkishMorphology.builder().setLexicon(
            RootLexicon.getDefault()
        ).ignoreDiacriticsInAnalysis().useInformalAnalysis().build()
    )

    analyses: java.util.ArrayList = (
        morphology.analyzeAndDisambiguate(text).bestAnalysis()
    )

    converter: InformalAnalysisConverter = (
        InformalAnalysisConverter(morphology.getWordGenerator())
    )

    for analysis in analyses:
        formal = formal + str(converter.convert(analysis.surfaceForm(), analysis)).split("-")[0] + " "
    print(formal)
    return formal,'''