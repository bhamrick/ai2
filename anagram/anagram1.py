def chars(s):
	return [sorted(s),s]
def second(t):
	return t[1]
wlist = sorted(map(chars,open("words.txt","r").read().split('\n')[:-1]))
prev = ['','']
lists = []
list = ''
for word in wlist:
	if sorted(word[-1])==sorted(prev[-1]):
		list = list + ', ' + word[-1]
	else:
		lists = lists + [[-len(list),list]]
		list = word[-1]
	prev=word
lists = sorted(lists)
for str in lists:
	if len(str[1]) >= 30:
		print str[1]
	else:
		break
