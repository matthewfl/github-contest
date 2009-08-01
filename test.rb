
$userList = {}
$repoList = {}
$ownerList = {}


class User
	attr_reader :follow, :id
	def initialize (name)
		@id = name
		@follow = []
	end
	def follow (repo)
		@follow.push repo
		repo.add self	
	end
	def follows
		return @follow
	end
	def think
		list = {}
		@follow.each do |rep|
			rep.follow.each do |usr|
				usr.follows.each do |vote|
					if !list[vote]
						list[vote] = 0
					end
					list[vote] += 1
				end
			end
		end
		@follow.each {|x| list[x] = 0}
		data = list.sort_by{|x,y| -y}.slice(0,10)
		"#{@id}:#{data.map{|x| x[0].id}.join(",")}"
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

class Repo
	attr_reader :follow, :name, :id, :path, :owner, :forked, :made
	def initialize (line)
		res = line.split(":")
		@id = res[0].to_i
		d = res[1].split(",")
		@path = d[0]
		p = d[0].split('/')
		@owner = $ownerList[p[0]] ||= Owner.new(p[0])
		@owner.add self
		@follow = [@owner]
		@name = p[1]
		@made = d[1]
		@forked = d[2]
	end
	def add (user)
		if user.is_a?(User)
			@follow.push user
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

puts "reading data"
File.open("data/data.txt") do |file|
	file.each do |line|
		user_id, repo_id = line.split(":")
		user = $userList[user_id.to_i] ||= User.new(user_id.to_i)
		user.follow($repoList[repo_id.to_i])
	end
end

puts "saving data"

File.open("data/test.txt") do |file|
	File.open("results.txt", "w") do |save|
		file.each do |line|
			user = $userList[line.to_i]
			out = "#{user.think}\n"
			puts out
			save << out
		end	
	end
end
