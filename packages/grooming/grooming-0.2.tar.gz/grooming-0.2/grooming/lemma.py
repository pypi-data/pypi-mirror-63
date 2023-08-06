"""
This package will clean the text and lemmatize it. This will return output as text

"""
from grooming import txt
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import wordnet
lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

def lemm(text,txt_clean=True,word_len = 3,ignore_lem=[]):
    """
    Description: Use this function to lemmatize the text.
    ---------

    Arguments:
    ---------
        txt: takes string as an input
        txt_clean: Default to True. Enabling it will clean the text.
        word_len: Default to 3. Length greater than this number will only be lemmatized
        ignore_lem: Default to blank. List of words which needs to be ignored in lemmatization process

    """
    try:
        clean_txt = str(text)
        if txt_clean:
            clean_txt = txt.cleaner(clean_txt)

        token = clean_txt.split(' ')
        token = [tok for tok in token if (tok not in ' ' or tok not in '') and len(tok)>3]
        lem = ''
        for t in token:
            if t.lower() not in ignore_lem:
                lem += lemmatizer.lemmatize(t.lower(), get_wordnet_pos(t))+' '
            else:
                lem+=t.lower()+' '
        clean_txt = str.rstrip(lem)
    except LookupError:
        import nltk
        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('averaged_perceptron_tagger')
        print('Downloaded the required packages. Please re-run the program')
    except Exception as e:
        print(e)
    return clean_txt
