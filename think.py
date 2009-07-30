import re

def debug(txt):
    print txt

class Think:
	# sub classes
	class User:
		def __init__(self):
			self.watch = []
		def add(self, n):
			self.watch.append(''.join(re.findall(Think.num, n)))
		def line(self):
			# print the line for saveing
			return ','.join([str(i) for i in self.watch[:10]])
	class Repo:
		def __init__(self,_id, info):
			self.id = _id
			self.lang = {}
			i = info.split(",")
			l = len(i)
			p = i[0].split("/", 1)
			self.path = i[0]
			self.owner = p[0]
			self.name = p[1]
			"""
			if l > 2:
				self.date = i[1]
			else:
				self.date = ""
			"""
			if l > 3:
				self.fork = i[2]
			else:
				self.fork = None
		def addLang(self, lang, lines):
			self.lang[lang] = lines
	class Lang:
		def __init__(self, name):
			self.name = name
			self.users = {}
		def add(self, repo):
			self.users[repo.path] = repo


	# const
	num = re.compile("[0-9]")

	def __init__(self):
		self.user = {}
		self.repo = {}
		self.lang = {}
	def loadData(self, name):
		with open(name) as f:
			for data in f:
				s = data.split(":")
				try:
					self.user[s[0]]
				except:
					self.user[s[0]] = Think.User()
				self.user[s[0]].add(s[1])
	
	def _langInfo(self, info):
		r = {}
		s = info.split(",")
		for i in s:
			l = i.split(";")
			r[l[0]] = int(l[1])
		return r
	
	def loadLang(self, name):
		with open(name) as f:
			for data in f:
				s = data.split(":", 1)
				info = self._langInfo(s[1])
				try:
					pro = self.repo[s[0]]
					for na in info:
						try:
							self.lang[na]
						except:
							self.lang[na] = Think.Lang(na)
						self.lang[na].add(pro)
						pro.addLang(na,info[na])
				except:
					pass
	
	def loadRepos(self, name):
		with open(name) as f:
			for data in f:
				s = data.split(":", 1)
				self.repo[s[0]] = Think.Repo(s[0], s[1])
	def save(self, name):
		with open(name, 'w') as f:
			for u in self.user:
				t = str(u) + ":" + self.user[u].line()
				f.write(t+"\n")

