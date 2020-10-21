import random
import string
import sys
from unicodedata import category
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize


def create_dictionary(filename):
    """Makes a histogram that contains the words from a file.

    filename: string

    returns: map from each word to the number of times it appears.
    """
    hist = {}
    fp = open(filename, encoding="UTF8")

    strippables = "".join(
        [chr(i) for i in range(sys.maxunicode) if category(chr(i)).startswith("P")]
    )

    for line in fp:
        line = line.replace("-", " ")

        for word in line.split():
            # word could be 'Sussex.'
            word = word.strip(strippables)
            word = word.lower()

            # update the dictionary
            hist[word] = hist.get(word, 0) + 1

    return hist


#  Question 1 - What are the top 10 frequent words in each text, with stopwords removed?


def most_common(hist):
    """Makes a list of word-freq pairs(tuples) in descending order of frequency that excludes stopwords.

    hist: map from word to frequency

    returns: list of (frequency, word) pairs
    """
    t = []
    stopwords = create_dictionary("data/stopwords.txt")
    stopwords = list(stopwords.keys())
    for word, freq in hist.items():
        if word in stopwords:
            continue
        t.append((freq, word))
    t.sort(reverse=True)
    return t


def print_most_common(hist, num=20):
    """Prints the most common words in a histogram and their frequencies.

    hist: histogram (map from word to frequency)
    num: number words to print
    """
    t = most_common(hist)
    print(f"The most common words are:")
    for freq, word in t[:num]:
        print(word, "\t", freq)


# Question 2 - Most frequent words that are not found in the other texts?
def nine_text_dictionary(text1, text2, text3, text4, text5, text6, text7, text8, text9):
    """combine all texts' dicionaries into 1 large dictionary.

    text1,text2, etc: each text hist dictionary
    return: combined dictionary"""

    nine_list = []
    for words in list(text1.keys()):
        nine_list.append(words)
    for words in list(text2.keys()):
        if words not in nine_list:
            nine_list.append(words)
        else:
            continue
    for words in list(text3.keys()):
        if words not in nine_list:
            nine_list.append(words)
        else:
            continue
    for words in list(text4.keys()):
        if words not in nine_list:
            nine_list.append(words)
        else:
            continue
    for words in list(text5.keys()):
        if words not in nine_list:
            nine_list.append(words)
        else:
            continue
    for words in list(text6.keys()):
        if words not in nine_list:
            nine_list.append(words)
        else:
            continue
    for words in list(text7.keys()):
        if words not in nine_list:
            nine_list.append(words)
        else:
            continue
    for words in list(text8.keys()):
        if words not in nine_list:
            nine_list.append(words)
        else:
            continue
    for words in list(text9.keys()):
        if words not in nine_list:
            nine_list.append(words)
        else:
            continue
    return nine_list


def unique_common_words(hist, other_texts):
    """common words that are unique for a text and not found in the other texts.

    returns: a list of words that are unique for this text."""
    unique_words = []
    for word, freq in hist.items():
        if word in other_texts:
            continue
        unique_words.append((freq, word))
    unique_words.sort(reverse=True)
    return unique_words


def print_most_Uniquely_common(hist, other_texts, num=20):
    """Prints the most common and unique words in a histogram and their frequencies.

    hist: histogram (map from word to frequency)
    num: number words to print
    """
    t = unique_common_words(hist, other_texts)
    print("The most common unique words are:")
    for freq, word in t[:num]:
        print(word, "\t", freq)


# Question 3. Analyze the tone of the entire book in order to compare.
def text_sensitive_analyzer(filename):
    """analyze the text to determine overall tone of book.
    PSUEDO CODE
    1. dictionary
    for each sentence:
    if sentences start with uppercase and ends with exclamation point
    2. then store it in variable called sent
    3. analyzer with variable
    store the normalized score aka compound in dictionary
    compute an average of the dictionary

    return: the compound(normalized) number of tone.
    """
    fp = open(filename, encoding="UTF8")
    data = fp.read()
    score = SentimentIntensityAnalyzer().polarity_scores(data)
    return score


Question 4. Test our hypothesis on two texts comparing and to see the text clustering of them.

def texts_clustering(filename1, filename2):
    """Test our hypothesis on two texts comparing them to see where they are clustered on a chart based on similarities.

    Used some code basis from: https://dev.to/coderasha/compare-documents-similarity-using-python-nlp-4odp

    Filenames: string
    Return: chart"""

    #TODO: to ask how to import gensim
    fp1 = open(filename1, encoding="UTF8")
    fp2 = open(filename2, encoding="UTF8")
    data1 = fp1.read()
    data2 = fp2.read()
    file1_sentence_list = []
    with open(data1) as f:  #TODO:  is it okay that we are doing data1 open instead of fp?
        tokens = sent_tokenize(f.read())
        for line in tokens:
            file1_sentence_list.append(line)
    gen_words_list = [
        [w.lower() for w in word_tokenize(text)] for text in file1_sentence_list
    ]
    dictionary = gensim.corpora.Dictionary(gen_words_list)
    corpus = [dictionary.doc2bow(gen_words_list) for gen_words_list in gen_words_list]
    tf_idf = gensim.models.TfidfModel(corpus)
    sims = gensim.similarities.Similarity(
        "data/workdir", tf_idf[corpus], num_features=len(dictionary)
    )  # TODO: is this index file that will be created correctly written?
    file2_sentence_list = []
    with open(data2) as f:
        tokens = sent_tokenize(f.read())
        for line in tokens:
            file2_sentence_list.append(line)
    for line in file2_sentence_list:
        query_doc = [w.lower() for w in word_tokenize(line)]
        query_doc_bow = dictionary.doc2bow(query_doc)
    create bag of words #TODO: is this correct?
    query_doc_tf_idf = tf_idf[query_doc_bow] #TODO: does this mean the s part of the equation for clustering?

    import numpy as np
    from sklearn.mainfold import MDS
    import matplotlib.pyplot as plt
    sum_of_sims = (np.sum(sims[query_doc_tf_idf], dtype = np.float32)) #TODO: ASK PROFESSOR: what does this do? is this just adding the similarities?
    # s = np.asarray()
    dissimilarities = 1-S
    coord = MDS(dissimilarity = 'precomputed').fit_transform(dissimilarities)
    plt.scatter(coord[:,0], coord[:,1])
    for i in range(coord.shape[0]):
        plt.annotate(str(i), (coord[i, :]))
    plt.show()


def main():
    """code that runs all the functions above to answer our questions with regards to the 10 texts."""
    # Create Dictionaries
    emma_hist = create_dictionary("data/emma.txt")
    men_hist = create_dictionary("data/little_men.txt")
    women_hist = create_dictionary("data/little_women.txt")
    mansfield_hist = create_dictionary("data/mansfield_park.txt")
    poirot_hist = create_dictionary("data/poirot_investigates.txt")
    pride_hist = create_dictionary("data/pride_and_prejudice.txt")
    sense_hist = create_dictionary("data/sense_and_sensibility.txt")
    cask_hist = create_dictionary("data/the_cask_of_amontillado.txt")
    brown_suit_hist = create_dictionary("data/the_man_in_the_brown_suit.txt")
    raven_hist = create_dictionary("data/the_raven.txt")

    # Number 1. Most Frequent Words
    # print_most_common(emma_hist)
    # print_most_common(men_hist)
    # print_most_common(women_hist)
    # print_most_common(mansfield_hist)
    # print_most_common(poirot_hist)
    # print_most_common(pride_hist)
    # print_most_common(sense_hist)
    # print_most_common(cask_hist)
    # print_most_common(brown_suit_hist)
    # print_most_common(raven_hist)

    # # Number 2. Most unique and common words
    # for_emma_hist = nine_text_dictionary(
    #     men_hist,
    #     women_hist,
    #     mansfield_hist,
    #     poirot_hist,
    #     pride_hist,
    #     sense_hist,
    #     cask_hist,
    #     brown_suit_hist,
    #     raven_hist,
    # )
    # for_men_hist = nine_text_dictionary(
    #     emma_hist,
    #     women_hist,
    #     mansfield_hist,
    #     poirot_hist,
    #     pride_hist,
    #     sense_hist,
    #     cask_hist,
    #     brown_suit_hist,
    #     raven_hist,
    # )
    # for_women_hist = nine_text_dictionary(
    #     emma_hist,
    #     men_hist,
    #     mansfield_hist,
    #     poirot_hist,
    #     pride_hist,
    #     sense_hist,
    #     cask_hist,
    #     brown_suit_hist,
    #     raven_hist,
    # )
    # for_mansfield_hist = nine_text_dictionary(
    #     emma_hist,
    #     men_hist,
    #     women_hist,
    #     poirot_hist,
    #     pride_hist,
    #     sense_hist,
    #     cask_hist,
    #     brown_suit_hist,
    #     raven_hist,
    # )
    # for_poirot_hist = nine_text_dictionary(
    #     emma_hist,
    #     men_hist,
    #     women_hist,
    #     mansfield_hist,
    #     pride_hist,
    #     sense_hist,
    #     cask_hist,
    #     brown_suit_hist,
    #     raven_hist,
    # )
    # for_pride_hist = nine_text_dictionary(
    #     emma_hist,
    #     men_hist,
    #     women_hist,
    #     mansfield_hist,
    #     poirot_hist,
    #     sense_hist,
    #     cask_hist,
    #     brown_suit_hist,
    #     raven_hist,
    # )
    # for_sense_hist = nine_text_dictionary(
    #     emma_hist,
    #     men_hist,
    #     women_hist,
    #     mansfield_hist,
    #     poirot_hist,
    #     pride_hist,
    #     cask_hist,
    #     brown_suit_hist,
    #     raven_hist,
    # )
    # for_cask_hist = nine_text_dictionary(
    #     emma_hist,
    #     men_hist,
    #     women_hist,
    #     mansfield_hist,
    #     poirot_hist,
    #     pride_hist,
    #     sense_hist,
    #     brown_suit_hist,
    #     raven_hist,
    # )
    # for_brown_suit_hist = nine_text_dictionary(
    #     emma_hist,
    #     men_hist,
    #     women_hist,
    #     mansfield_hist,
    #     poirot_hist,
    #     pride_hist,
    #     sense_hist,
    #     cask_hist,
    #     raven_hist,
    # )
    # for_raven_hist = nine_text_dictionary(
    #     emma_hist,
    #     men_hist,
    #     women_hist,
    #     mansfield_hist,
    #     poirot_hist,
    #     pride_hist,
    #     sense_hist,
    #     cask_hist,
    #     brown_suit_hist,
    # )
    # print_most_Uniquely_common(emma_hist, for_emma_hist)
    # print_most_Uniquely_common(men_hist, for_men_hist)
    # print_most_Uniquely_common(women_hist, for_women_hist)
    # print_most_Uniquely_common(mansfield_hist, for_mansfield_hist)
    # print_most_Uniquely_common(poirot_hist, for_poirot_hist)
    # print_most_Uniquely_common(pride_hist, for_pride_hist)
    # print_most_Uniquely_common(sense_hist, for_sense_hist)
    # print_most_Uniquely_common(cask_hist, for_cask_hist)
    # print_most_Uniquely_common(brown_suit_hist, for_brown_suit_hist)
    # print_most_Uniquely_common(raven_hist, for_raven_hist)

    # Question 3 Answers.
    # emma_average = text_sensitive_analyzer("data/emma.txt")
    # men_average = text_sensitive_analyzer("data/little_men.txt")
    # women_average = text_sensitive_analyzer("data/little_women.txt")
    # mansfield_average = text_sensitive_analyzer("data/mansfield_park.txt")
    # poirot_average = text_sensitive_analyzer("data/poirot_investigates.txt")
    # pride_average = text_sensitive_analyzer("data/pride_and_prejudice.txt")
    # sense_average = text_sensitive_analyzer("data/sense_and_sensibility.txt")
    # cask_average = text_sensitive_analyzer("data/the_cask_of_amontillado.txt")
    # brown_suit_average = text_sensitive_analyzer("data/the_man_in_the_brown_suit.txt")
    # raven_average = text_sensitive_analyzer("data/the_raven.txt")
    # print(f"The overall sentiment for Emma was {emma_average}")
    # print(f"The overall sentiment for Little Men was {men_average}")
    # print(f"The overall sentiment for Little Women was {women_average}")
    # print(f"The overall sentiment for Mansfield Park was {mansfield_average}")
    # print(f"The overall sentiment for Poirot Investigate was {poirot_average}")
    # print(f"The overall sentiment for Pride and Prejudice was {pride_average}")
    # print(f"The overall sentiment for Sense and Sensibility was {sense_average}")
    # print(f"The overall sentiment for The Cask of Amontillado was {cask_average}")
    # print(
    #     f"The overall sentiment for The Man in the Brown Suit was {brown_suit_average}"
    # )
    # print(f"The overall sentiment for The Raven was {raven_average}")

    #Question 4 Answers.
    # texts_clustering(filename1 = "data/emma.txt",filename2 = "data/the_raven.txt")


if __name__ == "__main__":
    main()