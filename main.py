#! /usr/bin/python
from think import Think


def main ():
	t = Think()
	print "loading repos"
	t.loadRepos("data/repos.txt")
	print "loading lang"
	t.loadLang("data/lang.txt")
	print "loading data"
	t.loadData("data/data.txt")
	print "saving data"
	t.save("results.txt")


if __name__ == "__main__":
	main()
