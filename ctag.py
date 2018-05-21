header = '''---
show: step
version: 1.0
enable_checker: true
---
'''
import os

def getListFiles(path):
	res = []
	for root,dirs,files in os.walk(path):
		for filepath in files:
			res.append(os.path.join(root,filepath))
	return res

def mdc(file):
	file = file.replace('\\','/')
	if not file.endswith('.md'):
		return
	with open(file,mode='r',encoding='utf-8') as f, open(file[:-3]+'1'+file[-3:],mode='w',encoding='utf-8') as f2:
		f2.write(header)
		n = 0
		for line in f:
			if line[:4].count('#')==2:
				n += 1
			if n==1:
				if line[:4].count('#')==3:
					line = "#### " + line[4:]
			f2.write(line)
	os.remove(file)
	os.rename(file[:-3]+'1'+'.md',file)

if __name__=='__main__':
	res = getListFiles(os.getcwd())
	for file in res:
		mdc(file)		
	print('done! Total:%d files.'%len(res))
		