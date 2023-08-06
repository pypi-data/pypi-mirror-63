#!/usr/bin/python3
# -*- coding: utf-8 -*-
from collections import OrderedDict
alphabet = list(map(chr, range(97, 123)))

d2r_dict=OrderedDict([
	('dar','डर'), 
	('malai','मलाई'),
	('hamro','हम्रो'),
	('napala','नेपाल'),
	('napala','नेपाल'), 
 	('surakshit','सुरक्षित'),
 	('suraksha','सुरक्षा'),
  	('suraksha','सुरक्षा'), 
	('thau','ठाउँ'),  
	('corona','कोरोना'),
	('aile','अहिले'),
	('aaile','अहिले'),
	('Covid19​','कोरोना'), 
	('SARS-CoV-2','कोरोना'), 
	('hoina','होइन'), 
	('koslai','कस्लाई'), 
	('khatarnak','खतरनाक'),
	('pariwartan','परिवर्तन'),  
	('kaslai','कस्लाई'), 
	('sambav','सम्भव'), 
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
	('xa','छ'),  
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
	('sa','स'),
	('wa','वा'), 
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
	('ma','म'),
	('za','श'),
	('ksha','क्ष'),
	('ksha','क्ष'),
	('la','ल'),
	('om','ओम'),
	('rri','रि'),
	('oo','ओ'),
	('na','न'),
	('ka','क'),
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
	Syntax:
	>>> nt.is_devanagari(text)

	Example:
		>>> import nepali_transliteration as nt
		>>> nt.is_devanagari("कोरोना")
			True

		>>> nt.romanize_text("nepalकोरोना")
			False

		>>> nt.romanize_text("corona")
			False
	"""
	if(sum(True for i in text if i.lower() in set(alphabet)) / len(text)) > 0.0:
		return False
	else:
		return True
   

def convert(text):
	"""
	This function can be used to convert romanize text into nepali.

	Syntax:
	>>> nt.convert(text)

	Example:
		>>> import nepali_transliteration as nt
		>>> nt.convert("corona")
			कोरोना
	"""
	text = text.lower()
	for key,value in d2r_dict.items():
		text=text.replace(key,value)  
	return text


def main():
     print(convert("nepal katiko Suraksha  cha"))


if __name__== "__main__":
  main()

