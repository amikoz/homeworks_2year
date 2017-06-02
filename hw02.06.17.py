import random
import codecs
from pymorphy2 import MorphAnalyzer
from pymystem3 import Mystem

morph = MorphAnalyzer()
m = Mystem()
corpus = dict()

with codecs.open("1grams-3.txt", encoding='utf-8') as ins:
    for line in ins:
        for word in line.split():
	    try:
                int(word)
	    except:
    		if word not in [',', '.', '%', '(', ')', ':', ';', '!', '-', "--", '"']:
    		    parsed_word = m.analyze(word)
		    if len(parsed_word) > 0:
			if parsed_word[0].get(u'analysis', None) is not None:
			    if len(parsed_word[0][u'analysis']) > 0:
				speech_part = parsed_word[0][u'analysis'][0]['gr'].replace("=", ',').split(',')[0]
				if corpus.get(speech_part, None) is None:
				    corpus[speech_part] = [parsed_word[0][u'text']]
				else:
				    corpus[speech_part].append(parsed_word[0][u'text'])

ana = m.analyze(u'Мама мыла раму')
for i in ana:
    if i.get(u'analysis', None) is not None:
        speech_part = i[u'analysis'][0]['gr'].split(',')[0].split('=')[0]
        print speech_part
        print i[u'analysis'][0]['gr']
        parsed_word = morph.parse(i[u'text'])
        tag = None
        for w in parsed_word:
            if w.tag.POS == grammems[speech_part]:
                tag = w.tag
        words_variant = morph.parse(random.choice(corpus[speech_part]))
        change = None
        for w in words_variant:
            if w.tag.POS == grammems[speech_part]:
                change = w
        print change.word
        current_grammemes = {k for k in tag.grammemes if k in ['sing', 'plur']}
        if speech_part == 'V':
            current_grammemes.update({'masc', 'femn', 'past', '1per', '2per', '3per', 'impr', 'indc', 'pres'})
        elif speech_part in ['S', 'PRTF', 'A']:
            current_grammemes.update({'nomn', 'gent', 'datv', 'accs', 'ablt'})
        print change.inflect(current_grammemes).word
