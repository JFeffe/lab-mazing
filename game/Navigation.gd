extends RefCounted
# Grid BFS deliberately excludes unexplored cells, locked doors and one-way airlocks.
static func passable(game,c):
	if not game.floor_at(c.x,c.y) or not game.seen.has(game.key(c.x,c.y)): return false
	for e in game.events:
		if Vector2i(e.cell[0],e.cell[1])==c:
			if e.kind=="oneway": return false
			if e.kind in ["door","exit","creature"] and not game.done.has(e.id): return false
	return true
static func route(game,start,goal):
	if not passable(game,goal): return []
	var queue=[start]
	var parents={start:start}
	var index=0
	while index<queue.size():
		var c=queue[index]
		index+=1
		if c==goal:
			var result=[c]
			while c!=start:
				c=parents[c]
				result.push_front(c)
			return result
		for d in [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]:
			var next=c+d
			if not parents.has(next) and passable(game,next):
				parents[next]=c
				queue.append(next)
	return []
