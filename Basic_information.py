import sys
import spacy
import pandas as pd
import json
import info 
import numpy as np
from dateparser.search import search_dates
from datetime import datetime
from word2number import w2n
from keywords import adult_keywords,child_keywords, pair_keywords, ambiguous_keywords,adults_keywords,childs_keywords,city_keywords 
from spacy.matcher import PhraseMatcher

nlp = spacy.load('en_core_web_lg')
# Set the phrase matcher
matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
city_terms = city_keywords 
patterns = [nlp.make_doc(city) for city in city_terms]
matcher.add('NZ_CITIES', patterns)

text = ' '.join(sys.argv[1:])
doc = nlp(text)
info = info.info


date_texts = []
matches = matcher(doc)
for match_id, start, end in matches:
    matched_city = doc[start:end].text
    prev_token = doc[start - 1] if start > 0 else None
    if prev_token and prev_token.lower_ == 'from':
        info["origin"] = matched_city
        info["origin_code"] = 1

# Iterate through the entities in the document
for ent in doc.ents:
    if ent.label_ == 'MONEY':
        info['money'] = ent.text.replace('¥', '').replace(',', '')
    elif ent.label_ in ['GPE', 'LOC','ORG','PERSON','FAC']:
        city_found = ent.text in city_keywords  
        prev_token = doc[ent.start - 1] if ent.start > 0 else None
        next_token = doc[ent.end] if ent.end < len(doc) else None

        if prev_token and prev_token.lower_ == 'from':
            info["origin"] = ent.text
            info["origin_code"] = 1 if city_found else -1
        elif prev_token and prev_token.lower_ == 'to':
            info["destination"] = ent.text
           
            if ent.text.lower() == 'new zealand' or not city_found:
                info["destination_code"] = -2 if ent.text.lower() == 'new zealand' else -1
            else:
                info["destination_code"] = 1
      
        elif next_token and (next_token.lower_ == 'starting' or next_token.lemma_ == 'start'):
            info["destination"] = ent.text
            info["destination_code"] = 1 if city_found else -1

        else:
            if info["origin"] is None:
                info["origin"] = ent.text
                info["origin_code"] = 1 if city_found else -1
            elif info["destination"] is None and info["origin"] is not None:
                info["destination"] = ent.text
                if ent.text.lower() == 'new zealand':
                    info["destination_code"] = -2
                else:
                    info["destination_code"] = 1 if city_found else -1

    elif ent.label_ == 'DATE':# If the entity is labeled 'DATE'
        date_texts.append(ent.text)


if info["destination"] is None:
    info["destination"] = "New Zealand"
    info["destination_code"] = -2

# Get the number around the word
def get_number_around(token):
    count = None

    if token.i > 0:
        prev_word = doc[token.i - 1].text.lower()
        if prev_word in ["a", "an"]:
            count = 1
        else:
            try:
                count = int(prev_word) if prev_word.isdigit() else w2n.word_to_num(prev_word)
            except ValueError:
                pass

   
    if token.i < len(doc) - 1 and count is None:
        next_word = doc[token.i + 1].text.lower()
        if next_word in ["a", "an"]:
            count = 1
        else:
            try:
                count = int(next_word) if next_word.isdigit() else w2n.word_to_num(next_word)
            except ValueError:
                pass

  
    if count is None:
        for ancestor in token.ancestors:
            try:
                count = w2n.word_to_num(ancestor.text.lower())
                break  
            except ValueError:
                continue
    return count




for token in doc:
    text = token.text.lower()
    if text in ["i", "me", "myself"] and not info["i_counted"]:
        info['adults'] += 1
        info["i_counted"] = True
    elif text in child_keywords:
        info['children'] += 1
    elif text in adult_keywords and text not in ["i", "me", "myself"]:
        info['adults'] += 1
    elif text in pair_keywords:
        num = get_number_around(token)  
        if num is None:
            num = 1 
        info['adults'] += num * 2 
    elif text in adults_keywords:
        num = get_number_around(token)
        info['adults'] += num if num is not None else -1  
    elif text in childs_keywords:
        num = get_number_around(token)
        info['children'] += num if num is not None else -1
    elif text in ambiguous_keywords:
        info['adults'] = -1
        info['children'] = -1
        break

# Count the total
if info['adults'] == -1 or info['children'] == -1:
    info['total_people'] = -1
else:
    info['total_people'] = info['adults'] + info['children']

del info["i_counted"]


def clean_date_text(date_text):
    date_text = date_text.replace('st', '').replace('nd', '').replace('rd', '').replace('th', '')
    date_text = date_text.replace('this year', '').strip()
    return date_text

if date_texts:
    date_str = clean_date_text(' '.join(date_texts))
    parsed_dates = search_dates(date_str)
    if parsed_dates:
        info['date'] = parsed_dates[0][1].strftime('%d/%m/%Y')
    else:
        info['date'] = "Date parsing failed"

print(json.dumps(info))
