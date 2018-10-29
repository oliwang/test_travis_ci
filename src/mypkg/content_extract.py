# coding: utf-8
from goose3 import Goose
from goose3.text import StopWordsChinese
import langid
import time

from newspaper import Article

g = Goose({'stopwords_class': StopWordsChinese})

def split_article2list(text, language, title):
    max_input = 1000
    period = "."
    if language == "zh_CN":
        max_input = 500
        period = "。"

    raw_split = text.replace("\n+", "\n").split("\n")
    #remove all empty lines
    raw_split = [s for s in raw_split if s != ""]

    index = 0
    text_list = []

    text_list.append({"index": index,
                      "text": title,
                      "src": ""})
    index = index + 1

    for i in range(0, len(raw_split)):
        raw_split_content = raw_split[i]
        if len(raw_split_content) < max_input:
            text_list.append({"index": index,
                              "text": raw_split_content,
                              "src": ""})
            index = index + 1
        else:
            indices = [i for i, x in enumerate(raw_split_content) if x == period]

            # "." could be from float numbers, use space after it to differentiate
            if language == "en_US":
                for i in indices:
                    if raw_split_content[i+1] == " ":
                        indices.remove(i)

            split_indices = []
            current_split_i = 0
            max_split_i = current_split_i + max_input

            for i in range(len(indices)):
                if (i+1 != len(indices)):
                    if (indices[i] < max_split_i and indices[i+1] >max_split_i):
                        split_indices.append(indices[i])
                        current_split_i = indices[i]
                        max_split_i = current_split_i + max_input

            split_tuples = []
            for i in range(len(split_indices)):
                if i == 0:
                    split_tuples.append((0, split_indices[i]))
                elif i == len(split_indices)-1:
                    split_tuples.append((split_indices[i-1] + 1, split_indices[i]))
                    split_tuples.append((split_indices[i]+1, len(raw_split_content)))
                else:
                    split_tuples.append((split_indices[i-1] + 1, split_indices[i]))

            new_list = [raw_split_content[s:e+1] for s,e in split_tuples]


            for i in range(len(new_list)):
                text_list.append({"index": index,
                              "text": new_list[i],
                              "src": ""})
                index = index + 1


    return text_list

def generate_content(url):
    a = Article(url)
    a.download()
    while a.download_state != 2:
        time.sleep(0.5)
    a.parse()

    languages = langid.classify(a.title)
    language = langid.classify(a.title)[0]

    if language != "en" and language != "zh":
        for l in languages:
            if l == "en":
                language = "en"
                break
            if l == "zh":
                language = "zh"
                break

    if language == "en":
        language = "en_US"
    elif language == "zh":
        language = "zh_CN"

    print(language)

    if a.text != "":
        print("1")
        return {"title": a.title, "text": a.text, "text_list": split_article2list(a.text, language, a.title), "language": language}
    elif language == "zh_CN":
        article = g.extract(url)
        print("2")
        return {"title": article.title, "text": article.cleaned_text, "text_list": split_article2list(article.cleaned_text, language, article.title), "language": language}
    else:
        print("3")
        return {"title": "", "text": "", "language": language, "msg": "We only support English and Chinese right now."}

if __name__ == "__main__":
    url = "https://www.cnn.com/2018/10/29/europe/angela-merkel-germany-election-intl/index.html"
    
    print(generate_content(url))

