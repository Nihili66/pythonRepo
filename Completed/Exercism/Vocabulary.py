def add_prefix_un(word):
    return 'un' + word


def make_word_groups(vocab_words):
    prefix = vocab_words[0]
    new_modified_list = [''.join((prefix, vocab_word)) for vocab_word in vocab_words[1:]]
    return ' :: '.join(([prefix] + new_modified_list))


def remove_suffix_ness(word: str):
    x = word[:-4]
    if x[-1] == 'i':
        return x[:-1] + 'y'
    else:
        return x


def adjective_to_verb(sentence: str, index):
    sentence_list = sentence.split(' ')
    adjective = sentence_list[index]
    if adjective[-1] == '.':
        return adjective[:-1] + 'en'
    else:
        return adjective + 'en'

