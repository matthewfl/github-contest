import re

def debug(txt):
    print txt

class Think:
    # sub classes
    class User:
        def __init__(self):
            self.watch = {}
            self.langs = {}
            self.langsFav = []
            self.langsSum = 0
            self._think = {}
            self._str = None
        def add(self, n):
            self.watch[''.join(re.findall(Think.num, n))] = 1
        def think(self, name):
            try:
                self.watch[name]
            except:
                try:
                    self._think[name]
                except:
                    self._think[name] = 0
                self._think[name] += 1
        def project(self, pro):
            pro.watchers.append(self)
            for l in pro.lang:
                try:
                    self.langs[l]
                except:
                    self.langs[l] = 0
                self.langs[l] += pro.lang[l]
        def friends(self, relate):
            for r in relate:
                l = r.watch
                for n in l:
                    self.think(n)
        def line(self):
            if self._str != None:
                return self._str
            # print the line for saveing
            data = self._think.items()
            data.sort(lambda x,y:(y[1] - x[1]))
            return ','.join([str(i[0]) for i in data[:10]])
        def done(self):
            # finished with the user object
            self._str = self.line()
            self._think = None
            self.langs = None
            return self._str
    class Owner:
        def __init__(self, name):
            self.name = name
            self.own = []
        def add(self, repo):
            self.own.append(repo)
    class Repo:
        def __init__(self, parent,_id, info):
            self.id = _id
            self.lang = {}
            self.links = []
            self.watchers = []
            i = info.split(",")
            l = len(i)
            p = i[0].split("/", 1)
            self.path = i[0]
            self.owner = p[0]
            self.name = p[1]
            # load the owner
            try:
                parent.owner[self.owner]
            except:
                parent.owner[self.owner] = Think.Owner(self.owner)
            parent.owner[self.owner].add(self)
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
        def link(self, other):
            pass
    class Lang:
        def __init__(self, name):
            self.name = name
            self.repos = {}
        def add(self, repo):
            self.repos[repo.path] = repo


    # const
    num = re.compile("[0-9]")
    FavLangMin = 50 # lines of code

    def __init__(self):
        self.user = {}
        self.repo = {}
        self.lang = {}
        self.owner = {}
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
                self.repo[s[0]] = Think.Repo(self, s[0], s[1])
    def save(self, name):
        with open(name, 'w') as f:
            for u in self.user:
                t = str(u) + ":" + self.user[u].line()
                f.write(t+"\n")
    
    def process1(self):
        for u in self.user:
            user = self.user[u]
            for p in user.watch:
                try:
                    user.project(self.repo[p])
                except:
                    pass
    def process2(self):
        for u in self.user:
            user = self.user[u]
            sum = 0
            for li in user.langs:
                sum += user.langs[li]
            user.langsSun = sum
            fav = user.langs.items()
            fav.sort(lambda x,y:(x[1] - y[1]))
            user.langsFav = fav[:3]
    def process3(self): # not used
        for p in self.repo:
            pro = self.repo[p]
            self.repo[p] = None
            #pro is the last pointer do what every you need here
            print pro.name
            for w in pro.watchers:
                w.friends(pro.watchers)
    def test(self, testName, saveName):
        with open(testName) as test:
            with open(saveName, 'w') as save:
                for us in test:
                    try:
                        u = ''.join(re.findall(Think.num, us))
                        out = u + ":"
                        user = self.user[u]
                        for rep in user.watch:
                            user.friends(self.repo[rep].watchers)
                        fav = user.langsFav
                        for th in user._think:
                            try:
                                ro = self.repo[th]
                                for fa in fav:
                                    if ro.lang[fa] > Think.FavLangMin:
                                        user.think(th)
                            except:
                                pass
                        out += user.done()
                        print "saving: ", out
                        save.write(out + "\n")
                    except:
                        pass
                    
