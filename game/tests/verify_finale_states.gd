extends SceneTree
const C=preload("res://FinaleControls.gd")
var failed=false
func _initialize():call_deferred("run")
func check(ok,text):
	if not ok:failed=true;push_error(text)
func descendants(node):
	var nodes=[]
	for child in node.get_children():nodes.append(child);nodes.append_array(descendants(child))
	return nodes
func run():
	var g=load("res://Main.tscn").instantiate();root.add_child(g);g.test_mode=true
	var oracle=JSON.parse_string(FileAccess.get_file_as_string("res://tests/chapter5_oracle.json"))
	var solutions=JSON.parse_string(FileAccess.get_file_as_string("res://tests/chapter5_solutions.json"))
	for n in range(21,26):
		g.start_game(false,n);g.close_modal();g.playing=false
		for e in g.events:
			if not e.has("puzzle_type"):continue
			if e.mode=="feedback":
				for token in oracle.feedback:
					var v=[]
					for bit in token:v.append(int(bit))
					v.append(1);check(C.solved(g,e,v)==oracle.feedback[token],"Independent graph oracle "+token)
					v[v.size()-1]=0;check(not C.solved(g,e,v),"Untested graph accepted")
			if e.has("world_gates"):
				g.done["installed_"+e.id]=true;var saved=C.initial(e);g.puzzle_states[e.id]=saved;g.sync_event(e)
				for gate in e.world_gates:
					if saved[int(gate.channel)]==0:continue
					var center=Vector3(gate.cell[0]*g.TILE,.1,gate.cell[1]*g.TILE)
					check(not g.floor_at(gate.cell[0],gate.cell[1]),"Gantry excluded from tap route")
					for direction in [-1,1]:
						g.player.position=center-Vector3.RIGHT*direction*g.TILE
						for frame in range(30):
							await physics_frame;g.player.velocity=Vector3.RIGHT*direction*g.MOVE_SPEED;g.player.velocity.y=-2;g.player.move_and_slide()
						check((g.player.position-center).x*direction<0,"Gantry collision bypass")
				g.player.position=Vector3(17*g.TILE,.1,5*g.TILE);g.show_puzzle(e)
				g.PuzzleControls.move(g,e,-2);check(g.puzzle_states[e.id]==saved,"Remote reset can strand player")
				check(not C.solved(g,e,[0,0,0]),"Unread inspections accepted")
				for id in e.observations:g.done[id]=true
				for state in oracle.gantry_states:
					var v=state.map(func(x):return int(x));g.puzzle_states[e.id]=v;g.sync_event(e)
					for b in e.world_gates:check(g.floor_at(b.cell[0],b.cell[1])==(v[int(b.channel)]==0),"Gantry geometry differs from state")
			var state=C.initial(e)
			for s in solutions[str(n)]:
				if s.id==e.id:
					for a in s.actions:C.move(e,state,int(a))
			check(C.solved(g,e,state),"Independent setup solution "+e.id)
			if e.mode in C.TESTED:
				var changed=state.duplicate();C.move(e,changed,99 if e.mode in C.PROGRAMS else 0)
				check(not C.solved(g,e,changed),"Editing reused test approval "+e.id)
			if e.mode=="courier":
				var changed=state.duplicate();C.move(e,changed,99);C.move(e,changed,98);check(not C.solved(g,e,changed),"Truncated route accepted")
			if e.mode=="dialogue":
				var changed=C.initial(e);C.move(e,changed,0);check(changed[0]==0 and changed[1]==1,"False promise advanced dialogue")
				C.move(e,state,99);check(state[0]==2 and not C.solved(g,e,state),"Dialogue undo")
			# All panels at actual Godot portrait/landscape logical scales in both languages.
			g.done["installed_"+e.id]=true
			for id in e.get("prerequisites",[]):g.done[id]=true
			g.done.erase(e.id);g.puzzle_states[e.id]=state
			for shape in [Vector2i(480,1039),Vector2i(960,444),Vector2i(1440,900)]:
				g.get_window().content_scale_size=shape;g.get_window().size=shape;g.configure_viewport()
				g.show_puzzle(e)
				for language in ["fr","en"]:
					g.localization.choose(language,false);g.show_puzzle(e)
					await process_frame;await process_frame;await process_frame
					check(g.modal_scroll.get_h_scroll_bar().max_value<=g.modal_scroll.size.x+1,"Horizontal overflow "+e.id+str(shape)+language)
					for node in descendants(g.modal_box):
						if node is Button:check(node.size.y>=38,"Touch button too small "+e.id)
			g.close_modal()
	print("FINALE: ORACLE + REVERSIBILITY + DYNAMIC COLLISIONS + FR/EN PORTRAIT/LANDSCAPE: ","FAIL" if failed else "PASS")
	quit(1 if failed else 0)
