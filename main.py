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
	print "processing 1"
	t.process1()
	print "processing 2"
	t.process2()
	# use the test file for this
	print "processing testing/saving"
	t.test("data/test.txt", "results.txt")
	#t.save("results.txt")


if __name__ == "__main__":
	main()
