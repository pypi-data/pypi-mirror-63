#!/usr/bin/python3
# -*- coding: utf-8 -*-

from collections import OrderedDict

d2r_dict=OrderedDict([
	('dar','डर'), 
	('malai','मलाई'),
	('napala','नेपाल'), 
	('thau','ठाउँ'),  
	('corona','कोरोना'), 
	('virus','भाइरस'), 
	('vairus','भाइरस'), 
	('co','को'), 
	('bha','भ'), 
	('ca','च'), 
	('tim','तिम्'), 
	('ti','ति'), 
	('ta','त'), 
	('rai','राई'), 
	('cha','छ'),
	('chha','छ'),  
	('da','द'), 
	('dha','ध'),
	('gha','घ'),    
	('fa','फा'),
	('pha','फ'),
	('ga','ग'), 
	('ra','र'),   
	('qa','का'), 
	('sha','श'),              
	('sh','श'), 
	('ta','त'),
	('tha','ठ'),
	('aa','आ'),
	('sa','स'),
	('wa','वा'), 
	('xa','क्ष'), 
	('ai','ई'), 

	('ya','या'), 
	('am','आम'), 
	('au','औ'), 
	('aum','ओम'), 

	('ja','ज'),
	('jha','झा'),
	('gya','ग्या'),
	('yan','यन'),
	('nga','ङ्ग'),
	('ma','झा'),
	('za','श'),
	('ksha','क्ष'),
	('ksha','क्ष'),
	('la','ल'),
	('om','ओम'),
	('rri','रि'),
	('oo','ओ'),
	('na','न'),
	('ja','ज'),
	('a','ा'), 
	('b','ब'), 
	('c','च'), 
	('d','द'), 
	('e','े'), 
	('f','उ'), 
	('g','ग'), 
	('h','ह'), 
	('i','ि'), 
	('j','ज'), 
	('k','क'), 
	('l','ल'), 
	('n','न'), 
	('m','म'), 
	('o','ो'),
	('pa','प'), 
	('p','प'), 
	('q','ट'), 
	('r','र'), 
	('s','स'), 
	('t','त'), 
	('u','ु'), 
	('v','व'), 
	('w','ौ'), 
	('x','ड'), 
	('y','य'), 
	('z','ष')
	])

def is_devanagari(text):
    """
    This function checks if the text is in Devanagari format.

    Detail description:
    In the text, it ignores all the punctuations, white spaces and other non-alphanumeric characters and then counts the
    number of devanagari characters. If the number of devanagari characters is more than or equal to 50% of the stripped
    text, the function deems the text devanagari, otherwise not.

    Syntax:
    >>> nt.is_devanagari(text)

    Example:
        >>> import nepali_transliteration as nt
        >>> nt.is_devanagari("नगरपालिका")
            True

        >>> nt.romanize_text("surajपालिक")
            False

        >>> nt.romanize_text("suraj")
            False
    """
    # text = "".join(i for i in text if i.isalnum())
    # print(text)
    return (sum(True for i in text if ord(i) in range(2304, 2432)) / len(text)) >= 0.5
   

def convert(text):
    """
    This function can be used to romanize the Nepali text to English.

    Syntax:
    >>> nt.convert(text)

    Example:
        >>> import nepali_roman as nt
        >>> nt.convert("nagarapaalikaa")
            नगरपालिका
    """
	for key,value in d2r_dict.items():
		text=text.replace(key,value)  
    return text
