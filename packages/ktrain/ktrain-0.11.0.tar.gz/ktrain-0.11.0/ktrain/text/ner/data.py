
from ...imports import *
from ... import utils as U
from . import preprocessor as pp
from .preprocessor import NERPreprocessor

from .anago.preprocessing import IndexTransformer, ELMoTransformer


MAXLEN = 128
WORD_COL = 'Word'
TAG_COL = 'Tag'
SENT_COL = 'SentenceID'



def entities_from_gmb(train_filepath, 
                      val_filepath=None,
                      wv_path_or_url=None,
                      use_elmo=False,
                      word_column=WORD_COL,
                      tag_column=TAG_COL,
                      sentence_column=SENT_COL,
                       encoding='latin1',
                       val_pct=0.1, verbose=1):
    """
    Loads sequence-labeled data from text file in the  Groningen
    Meaning Bank  (GMB) format.
    """


    return entities_from_txt(train_filepath=train_filepath,
                             val_filepath=val_filepath,
                             wv_path_or_url=wv_path_or_url,
                             use_elmo=use_elmo,
                             word_column=word_column,
                             tag_column=tag_column,
                             sentence_column=sentence_column,
                             data_format='gmb',
                             encoding=encoding,
                             val_pct=val_pct, verbose=verbose)


        
def entities_from_conll2003(train_filepath, 
                            val_filepath=None,
                            wv_path_or_url=None,
                            use_elmo=False,
                            encoding='latin1',
                            val_pct=0.1, verbose=1):
    """
    Loads sequence-labeled data from a file in CoNLL2003 format.
    """
    return entities_from_txt(train_filepath=train_filepath,
                             val_filepath=val_filepath,
                             wv_path_or_url=wv_path_or_url,
                             use_elmo=use_elmo,
                             data_format='conll2003',
                             encoding=encoding,
                             val_pct=val_pct, verbose=verbose)




def entities_from_txt(train_filepath, 
                      val_filepath=None,
                      wv_path_or_url=None,
                      use_elmo=False,
                      word_column=WORD_COL,
                      tag_column=TAG_COL,
                      sentence_column=SENT_COL,
                      data_format='conll2003',
                      encoding='latin1',
                      val_pct=0.1, verbose=1):
    """
    Loads sequence-labeled data from comma or tab-delmited text file.
    Format of file is either the CoNLL2003 format or Groningen Meaning
    Bank (GMB) format - specified with data_format parameter.

    In both formats, each word appars on a separate line along with
    its associated tag (or label).  
    The last item on each line should be the tag or label assigned to word.
    
    In the CoNLL2003 format, there is an empty line after
    each sentence.  In the GMB format, sentences are deliniated
    with a third column denoting the Sentence ID.


    
    More information on CoNLL2003 format: 
       https://www.aclweb.org/anthology/W03-0419

    CoNLL Example (each column is typically separated by space or tab)
    and  no column headings:

       Paul	B-PER
       Newman	I-PER
       is	O
       a	O
       great	O
       actor	O
       !	O

    More information on GMB format:
    Refer to ner_dataset.csv on Kaggle here:
       https://www.kaggle.com/abhinavwalia95/entity-annotated-corpus/version/2

    GMB example (each column separated by comma or tab)
    with column headings:

      SentenceID   Word     Tag    
      1            Paul     B-PER
      1            Newman   I-PER
      1            is       O
      1            a        O
      1            great    O
      1            actor    O
      1            !        O
    

    Args:
        train_filepath(str): file path to training CSV
        val_filepath (str): file path to validation dataset
        wv_path_or_url(str): either a URL or file path toa fasttext word vector file (.vec or .vec.zip or .vec.gz)

                             Example valid values for wv_path_or_url:
                               Randomly-initaialized word embeddings:
                                 set wv_path_or_url=None
                               English pretrained word vectors:
                                 https://dl.fbaipublicfiles.com/fasttext/vectors-english/crawl-300d-2M.vec.zip
                               Chinese pretrained word vectors:
                                 https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.zh.300.vec.gz
                               Russian pretrained word vectors:
                                 https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.ru.300.vec.gz
                               Dutch pretrained word vectors:
                                 https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.nl.300.vec.gz


                             See these two Web pages for a full list of URLs to word vector files for 
                             different languages:
                                1.  https://fasttext.cc/docs/en/english-vectors.html (for English)
                                2.  https://fasttext.cc/docs/en/crawl-vectors.html (for non-English langages)

                            Default:None (randomly-initialized word embeddings are used)

        use_elmo(bool):    If True, Elmo embeddings will be used in addition to word/character embeddings
        word_column(str): name of column containing the text
        tag_column(str): name of column containing lael
        sentence_column(str): name of column containing Sentence IDs
        data_format(str): one of colnll2003 or gmb
                          word_column, tag_column, and sentence_column
                          ignored if 'conll2003'
        encoding(str): the encoding to use
        val_pct(float): Proportion of training to use for validation.
        verbose (boolean): verbosity
    """



    # set dataframe converter
    if data_format == 'gmb':
        data_to_df = gmb_to_df
    else:
        data_to_df = conll2003_to_df
        word_column, tag_column, sentence_column = WORD_COL, TAG_COL, SENT_COL

    # create dataframe
    train_df = data_to_df(train_filepath, encoding=encoding)


    val_df = None if val_filepath is None else data_to_df(val_filepath, encoding=encoding)
    return entities_from_df(train_df,
                            val_df=val_df,
                            word_column=word_column,
                            tag_column=tag_column,
                            sentence_column=sentence_column,
                            wv_path_or_url=wv_path_or_url,
                            use_elmo=use_elmo,
                            val_pct=val_pct, verbose=verbose)



def entities_from_df(train_df,
                     val_df=None,
                     word_column=WORD_COL,
                     tag_column=TAG_COL,
                     sentence_column=SENT_COL,
                     wv_path_or_url=None,
                     use_elmo=False,
                     val_pct=0.1, verbose=1):
    """
    Load entities from pandas DataFrame
    Args:
      train_df(pd.DataFrame): training data
      val_df(pdf.DataFrame): validation data
      word_column(str): name of column containing the text
      tag_column(str): name of column containing lael
      sentence_column(str): name of column containing Sentence IDs

        wv_path_or_url(str): either a URL or file path toa fasttext word vector file (.vec or .vec.zip or .vec.gz)

                             Example valid values for wv_path_or_url:
                               Randomly-initialized word vectors:
                                 set wv_path_or_url=None
                               English pretrained word vectors:
                                 https://dl.fbaipublicfiles.com/fasttext/vectors-english/crawl-300d-2M.vec.zip
                               Chinese pretrained word vectors:
                                 https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.zh.300.vec.gz
                               Russian pretrained word vectors:
                                 https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.ru.300.vec.gz
                               Dutch pretrained word vectors:
                                 https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.nl.300.vec.gz


                             See these two Web pages for a full list of URLs to word vector files for 
                             different languages:
                                1.  https://fasttext.cc/docs/en/english-vectors.html (for English)
                                2.  https://fasttext.cc/docs/en/crawl-vectors.html (for non-English langages)


                            Default:None (randomly-initialized word embeddings are used)

     use_elmo(bool):    If True, Elmo embeddings will be used in addition to word/character embeddings
     verbose (boolean): verbosity

    """
    # process dataframe and instantiate NERPreprocessor
    x, y  = pp.process_df(train_df, 
                          word_column=word_column,
                          tag_column=tag_column,
                          sentence_column=sentence_column,
                          verbose=verbose)

    # get validation set
    if val_df is None:
        x_train, x_valid, y_train, y_valid = train_test_split(x, y, test_size=val_pct)
    else:
        x_train, y_train = x, y
        (x_valid, y_valid)  = pp.process_df(val_df,
                                            word_column=word_column,
                                            tag_column=tag_column,
                                            sentence_column=sentence_column,
                                            verbose=0)

    # preprocess and convert to generator
    if use_elmo:
        p = ELMoTransformer(use_char=True)
    else:
        p = IndexTransformer(use_char=True)
    preproc = NERPreprocessor(p, wv_path_or_url=wv_path_or_url, use_elmo=use_elmo)
    preproc.fit(x_train, y_train)
    trn = pp.NERSequence(x_train, y_train, batch_size=U.DEFAULT_BS, p=p)
    val = pp.NERSequence(x_valid, y_valid, batch_size=U.DEFAULT_BS, p=p)

    return ( trn, val, preproc)



def entities_from_array(x_train, y_train,
                        x_test=None, y_test=None,
                        wv_path_or_url=None,
                        use_elmo=False,
                        verbose=1):
    """
    Load entities from arrays
    Args:
      x_train(list): list of list of entity tokens for training
                     Example: x_train = [['Hello', 'world'], ['Hello', 'Cher'], ['I', 'love', 'Chicago']]
      y_train(list): list of list of tokens representing entity labels
                     Example:  y_train = [['O', 'O'], ['O', 'B-PER'], ['O', 'O', 'B-LOC']]
      x_test(list): list of list of entity tokens for validation 
                     Example: x_train = [['Hello', 'world'], ['Hello', 'Cher'], ['I', 'love', 'Chicago']]
      y_test(list): list of list of tokens representing entity labels
                     Example:  y_train = [['O', 'O'], ['O', 'B-PER'], ['O', 'O', 'B-LOC']]
        wv_path_or_url(str): either a URL or file path toa fasttext word vector file (.vec or .vec.zip or .vec.gz)

                             Example valid values for wv_path_or_url:
                               Randomly-initialized word embeeddings:
                                 set wv_path_or_url=None
                               English pretrained word vectors:
                                 https://dl.fbaipublicfiles.com/fasttext/vectors-english/crawl-300d-2M.vec.zip
                               Chinese pretrained word vectors:
                                 https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.zh.300.vec.gz
                               Russian pretrained word vectors:
                                 https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.ru.300.vec.gz
                               Dutch pretrained word vectors:
                                 https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.nl.300.vec.gz


                             See these two Web pages for a full list of URLs to word vector files for 
                             different languages:
                                1.  https://fasttext.cc/docs/en/english-vectors.html (for English)
                                2.  https://fasttext.cc/docs/en/crawl-vectors.html (for non-English langages)

                            Default:None (randomly-initialized word embeddings are used)

     use_elmo(bool):    If True, Elmo embeddings will be used in addition to word/character embeddings
     verbose (boolean): verbosity

    """
    # TODO: converting to df to use entities_from_df - needs to be refactored
    train_df = array_to_df(x_train, y_train) 
    val_df = None
    if x_test is not None and y_test is not None:
        val_df = array_to_df(x_test, y_test)
    if verbose:
        print('training data sample:')
        print(train_df.head())
        print('validation data sample:')
        print(val_df.head())
    return entities_from_df(train_df, val_df=val_df, 
                            wv_path_or_url=wv_path_or_url, use_elmo=use_elmo, verbose=verbose)






def array_to_df(x_list, y_list):
    ids = []
    words = []
    tags = []
    for idx, lst in enumerate(x_list):
        length = len(lst)
        words.extend(lst)
        tags.extend(y_list[idx])
        ids.extend([idx] * length)
    return pd.DataFrame(zip(ids, words, tags), columns=[SENT_COL, WORD_COL, TAG_COL])




def conll2003_to_df(filepath, encoding='latin1'):
    # read data and convert to dataframe
    sents, words, tags = [],  [], []
    sent_id = 0
    docstart = False
    with open(filepath, encoding=encoding) as f:
        for line in f:
            line = line.rstrip()
            if line:
                if line.startswith('-DOCSTART-'): 
                    docstart=True
                    continue
                else:
                    docstart=False
                    parts = line.split()
                    words.append(parts[0])
                    tags.append(parts[-1])
                    sents.append(sent_id)
            else:
                if not docstart:
                    sent_id +=1
    df = pd.DataFrame({SENT_COL: sents, WORD_COL : words, TAG_COL:tags})
    df = df.fillna(method="ffill")
    return df


def gmb_to_df(filepath, encoding='latin1'):
    df = pd.read_csv(filepath, encoding=encoding)
    df = df.fillna(method="ffill")
    return df




