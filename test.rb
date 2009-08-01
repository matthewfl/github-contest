
$userList = {}
$repoList = {}
$repoName = {}
$ownerList = {}



class User
	attr_reader :follow, :id
	def initialize (name)
		@id = name
		@follow = []
		@langs = {}
	end
	def follow (repo)
		if repo.is_a?(Repo)
			@follow.push repo
			repo.add self
			repo.langs.each do |name, lines|
				if !@langs[name]
					@langs[name] = 0
				end
				@langs[name] += lines
			end
		end	
	end
	def follows
		@follow
	end
	def think
		list = {}
		favLang = @langs.sort_by{|x,y| -y}.slice(0,3).map{|x| x[0]}
		@follow.each do |rep|
			rep.follow.each do |usr|
				usr.follows.each do |vote|
					if !list[vote]
						list[vote] = 0
					end
					list[vote] += vote.value
				end
			end
			rep.might.each do |vote|
				if !list[vote]
					list[vote] = 0
				end
				list[vote] += vote.value
			end
		end
		list.each do |r, votes|
			favLang.each do |x|
				if r.langs[x] and r.langs[x] > 100
					votes += r.value
				end
			end
		end
		@follow.each {|x| list[x] = 0}
		data = list.sort_by{|x,y| -y}.slice(0,10)
		"#{@id}:#{data.slice(0,@follow.length).map{|x| x[0].id}.join(",")}"
	end
end

class Owner
	attr_reader :name, :own
	def initialize (name)
		@name = name
		@own = []
	end
	def follows
		@own
	end
	def add (r)
		if r.is_a?(Repo)
			@own.push r
		end
	end
end

class VoidOwner < Owner
	def follows
		[]
	end
	def add (r)
	end
end
$voidOwner = VoidOwner.new("")

class Repo
	attr_reader :follow, :name, :id, :path, :owner, :forked, :made, :value, :might
	attr_accessor :children, :langs
	def initialize (line)
		@value = 1
		@langs = {}
		if line.is_a? String
			res = line.split(":")
			@id = res[0].to_i
			d = res[1].split(",")
			@path = d[0]
			p = d[0].split('/')
			@owner = $ownerList[p[0]] ||= Owner.new(p[0])
			@owner.add self
			@follow = [@owner]
			@might = []
			@name = p[1]
			@made = d[1]
			@forked = d[2]
			@children = []
		else
			@id = line
			@path = ""
			@owner = $voidOwner
			@follow = []
			@might = []
			@name = ""
			@made = ""
			@forked = nil
			@children = []
		end
	end
	def add (user)
		if user.is_a?(User)
			@follow.push user
		end
	end
	def process
		if @follow.length > 200
			@value = 0.5
		end
		@name.scan(/[A-Za-z]*/).each do |what|
			if !what.empty?
				n = ($repoName[what] ||= [])
				n.push self
			end
		end
		if @forked
			@forked = $repoList[@forked.to_i] ||= Repo.new(@forked.to_i)
			@might.push @forked
			@forked.children.push self
		end
	end
	def mights (repos)
		@might += repos
	end
	def process3
		if @forked
			@might += @forked.children || []
		end
	end
end



puts "reading repos"
File.open("data/repos.txt") do |file|
	file.each do |line|
		r = Repo.new(line)
		$repoList[r.id] = r
	end
end

puts "reading langs"
File.open ("data/lang.txt") do |file|
	file.each do |line|
		d = line.strip.split(":")
		r = $repoList[d[0].to_i] ||= Repo.new(d[0].to_i)
		langs = d[1].split(',')
		langs.each do |lang|
			l = lang.split(';')
			r.langs[l[0]] = l[1].to_i
		end
	end
end

puts "reading data"
File.open("data/data.txt") do |file|
	file.each do |line|
		user_id, repo_id = line.split(":")
		user = $userList[user_id.to_i] ||= User.new(user_id.to_i)
		user.follow($repoList[repo_id.to_i])
	end
end


puts "processing repos"
puts "1"
$repoList.each { |name, repo|
	repo.process
}

puts "2"
$repoName.each do |name, repos|
	if !name.empty?
		puts "\t#{name}"
		repos.each {|x| x.mights repos}
	end
end
puts "3"
$repoList.each { |name, repo|
	repo.process3
}

puts "saving data"

File.open("data/test.txt") do |file|
	File.open("results.txt", "w") do |save|
		file.each do |line|
			user = $userList[line.to_i]
			if user
				out = "#{user.think}\n"
				puts out
				save << out
			end
		end	
	end
end
