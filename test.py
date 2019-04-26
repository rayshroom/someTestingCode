from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn


def penn_to_wn(tag):
    """ Convert between a Penn Treebank tag to a simplified Wordnet tag """
    if tag.startswith('N'):
        return 'n'

    if tag.startswith('V'):
        return 'v'

    if tag.startswith('J'):
        return 'a'

    if tag.startswith('R'):
        return 'r'

    return None


def tagged_to_synset(word, tag):
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None
    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None


def sentence_similarity(sentence1, sentence2):
    # Tokenize and tag
    sentence1 = pos_tag(word_tokenize(sentence1))
    sentence2 = pos_tag(word_tokenize(sentence2))

    # Get the synsets for the tagged words
    synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in sentence1]
    synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence2]

    # Filter out the Nones
    synsets1 = [ss for ss in synsets1 if ss]
    synsets2 = [ss for ss in synsets2 if ss]



    score, count = 0.0, 0
#    best_score = 0
    scores = []
    # For each word in the first sentence
    for synset in synsets1:
        for ss in synsets2:
            if (synset.path_similarity(ss)) is not None:
                scores.append(synset.path_similarity(ss))
        # Get the similarity value of the most similar word in the other sentence
        #best_score = max([synset.path_similarity(ss) for ss in synsets2 if synset.path_similarity(ss) is not None])

        # Check that the similarity could have been computed
        if scores is not None and len(scores) != 0:
            score += max(scores)
            count += 1

    # Average the values
    score /= count
    return score


def symmetric_sentence_similarity(sentence1, sentence2):
    return (sentence_similarity(sentence1, sentence2) + sentence_similarity(sentence2, sentence1)) / 2


sentences = [
    "Apple Inc., now a trillion-dollar behemoth on the popularity of its high-priced devices, is banking its future on subscription services.",
    "Apple Inc., is banking its future on subscription services.",
    "Google Inc., is banking its future on subscription services.",
    "Apple Inc. is all-in on monthly subscription services.",
    "Google Inc. has put its future on subscription services.",
    "Apple Inc., now a trillion-dollar behemoth on the popularity of its high-priced devices"
]

focus_sentence = "Apple Inc., a company that became a trillion-dollar behemoth on the popularity of its sleek and high-priced devices, is banking its future on subscription services."

for sentence in sentences:
    print("Similarity(\"%s\", \"%s\") = %s" % (focus_sentence, sentence, symmetric_sentence_similarity(focus_sentence, sentence)))
    #print("Similarity(\"%s\", \"%s\") = %s" % (sentence, focus_sentence, symmetric_sentence_similarity(sentence, focus_sentence)))


'''

Similarity("Apple Inc., a company that became a trillion-dollar behemoth on the popularity of its sleek and high-priced devices, is banking its future on subscription services.", "Apple Inc., now a trillion-dollar behemoth on the popularity of its high-priced devices, is banking its future on subscription services.") = 1.0
Similarity("Apple Inc., a company that became a trillion-dollar behemoth on the popularity of its sleek and high-priced devices, is banking its future on subscription services.", "Apple Inc., is banking its future on subscription services.") = 1.0
Similarity("Apple Inc., a company that became a trillion-dollar behemoth on the popularity of its sleek and high-priced devices, is banking its future on subscription services.", "Google Inc., is banking its future on subscription services.") = 0.669017094017094
Similarity("Apple Inc., a company that became a trillion-dollar behemoth on the popularity of its sleek and high-priced devices, is banking its future on subscription services.", "Apple Inc. is all-in on monthly subscription services.") = 1.0
Similarity("Apple Inc., a company that became a trillion-dollar behemoth on the popularity of its sleek and high-priced devices, is banking its future on subscription services.", "Google Inc. has put its future on subscription services.") = 0.5066239316239316
Similarity("Apple Inc., a company that became a trillion-dollar behemoth on the popularity of its sleek and high-priced devices, is banking its future on subscription services.", "Apple Inc., now a trillion-dollar behemoth on the popularity of its high-priced devices") = 1.0

Similarity("Apple Inc., is banking its future on subscription services.", "Google Inc., is banking its future on subscription services.") = 0.8466880341880342

'''