from nltk import download, word_tokenize, pos_tag
from nltk.corpus import stopwords, gutenberg, wordnet
from nltk.stem import WordNetLemmatizer
from nltk import FreqDist
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
from collections import Counter


text = gutenberg.raw('Moby_dick.txt')
def get_wordnet_pos(treebank_tag):
    return {
        'J': wordnet.ADJ,
        'V': wordnet.VERB,
        'N': wordnet.NOUN,
        'R': wordnet.ADV
    }.get(treebank_tag[0], wordnet.NOUN)

stop_words = set(stopwords.words("english"))
tokens = [
    word for word in word_tokenize(text.lower())
    if word.isalnum() and word not in stop_words
]
pos_tags = pos_tag(tokens)
pos_freq = Counter(tag for word, tag in pos_tags).most_common(5)
print("The 5 most common parts of speech:", pos_freq)
lemmatizer = WordNetLemmatizer()
lemmatized_tokens = [
    (lemmatizer.lemmatize(word, get_wordnet_pos(tag)), tag)
    for word, tag in pos_tags
][:20]
print("\nLemmatized tokens (top 20):", lemmatized_tokens)

plt.figure(figsize=(12, 6))
plt.bar(*zip(*Counter(tag for word, tag in pos_tags).items()))
plt.xlabel('All Parts of The Speech')
plt.ylabel('Frequency')
plt.title('Frequency Distribution')
plt.show()
