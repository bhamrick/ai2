wlist = open("words","r").read().split('\n')[:-1]
def counts(str):
	ans = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	for c in list(str):
		if ord(c) >= ord('a') and ord(c) <= ord('z'):
			ans[ord(c)-ord('a')]+=1
	return ans
def dominates(c1, c2): #Returns true if every element of c1 is at least the corresponding element of c2
	for i in range(0,min(len(c1),len(c2))):
		if  c2[i]>c1[i]:
			return False
	return True
c = counts(raw_input('Enter a string: '))
ans = []
for word in wlist:
	if len(word) >= 3:
		if dominates(c,counts(word)):
			ans += [[len(word),word]]
ans = sorted(ans)
for pair in ans:
	print pair[1]
