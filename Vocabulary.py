vocabulary = {"apple": ["яблоко", "яблоня"],
              "cat": ["кошка"],
              "dog": ["собака"]
              }


def add_word(vocab, word, translation):
    word = word.strip().lower()
    translation = translation.strip().lower()
    if word in vocab:
        print("Слово в словаре уже есть")
        if translation in vocabulary[word]:
            print(f"Перевод '{translation}' к слову '{word}' уже написан")
        else:
            vocab[word].append(translation)
            print(f"Добавлен перевод '{translation}' для слова '{word}'")
    else:
        vocab[word] = [translation]


add_word(vocabulary, "cat", "кошка")
add_word(vocabulary, "sheep", "овца")
print(vocabulary)
