# Brian Hamrick
# 9/4/08
# Anagrammer
# Input: A six letter word to be anagrammed and the dictionary file "words.txt"
# Process: Check the other words in the dictionary and
#          print them if they are anagrams of the input
# Output: A list of anagrams of the input word

wlist = open("words.txt","r").read().split('\n')[:-1]
ustr = raw_input('Enter a word or *quit* to quit: ')
while ustr != '*quit*':
	count = 0
	for word in wlist:
		if sorted(word)==sorted(ustr) and word!=ustr:
			count+=1
			print '%d: %s' % (count, word)
	if count==0:
		print 'No anagrams'
	ustr = raw_input('\nEnter a word or *quit* to quit: ')

