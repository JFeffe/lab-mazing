extends SceneTree
const C=preload("res://CertaintyControls.gd")
var failed=false
func _initialize():call_deferred("run")
func check(ok,text):
 if not ok:failed=true;push_error(text)
func run():
 var g=load("res://Main.tscn").instantiate();root.add_child(g);g.test_mode=true
 var oracle=JSON.parse_string(FileAccess.get_file_as_string("res://tests/chapter4_network_oracle.json"))
 for n in range(16,21):
  g.start_game(false,n);g.close_modal()
  for e in g.events:
   if not e.has("puzzle_type"):continue
   if e.id in oracle:
    for mask in range(1<<e.edges.size()):
     var v=[]
     for i in range(e.edges.size()):v.append((mask>>i)&1)
     var expected=false
     for good in oracle[e.id]:
      if v==good.map(func(x):return int(x)):expected=true
     v.append(1)
     check(C.solved(g,e,v)==expected,"Network state differs from independent oracle "+e.id+str(mask))
     v[v.size()-1]=0;check(not C.solved(g,e,v),"Untested route accepted")
   if e.has("world_gates"):
    g.done["installed_"+e.id]=true
    g.player.position=Vector3(e.cell[0]*g.TILE,.1,e.cell[1]*g.TILE)
    var v=C.initial(e)
    if n==16:C.move(e,v,2)
    if n==17:C.move(e,v,1)
    if n==18:C.move(e,v,0);C.move(e,v,98)
    check(not C.solved(g,e,v),"Missing physical observations accepted")
    g.puzzle_states[e.id]=v;g.sync_event(e)
    var saved=v.duplicate();g.player.position=Vector3(g.start_cell.x*g.TILE,.1,g.start_cell.y*g.TILE)
    # Far from console: reset and changes cannot strand player through a remote panel.
    if not C.can_move(g,e):
     g.show_puzzle(e);g.PuzzleControls.move(g,e,-2);check(g.puzzle_states[e.id]==saved,"Remote reset changed gates")
    # Closed gates physically stop both directions and are excluded from tap navigation.
    for gate in e.world_gates:
     if v[int(gate.channel)] in gate.allowed.map(func(x):return int(x)):continue
     var center=Vector3(gate.cell[0]*g.TILE,.1,gate.cell[1]*g.TILE)
     var direction=Vector3.BACK if n==16 else Vector3.RIGHT
     check(not g.floor_at(gate.cell[0],gate.cell[1]),"Closed gate remains walkable")
     for sign_v in [-1,1]:
      g.player.position=center-direction*sign_v*g.TILE
      for frame in range(30):
       await physics_frame;g.player.velocity=direction*sign_v*g.MOVE_SPEED;g.player.velocity.y=-2;g.player.move_and_slide()
      check((g.player.position-center).dot(direction)*sign_v<0,"Dynamic gate collision bypass")
   if e.mode=="assembly":
    for order in [[0,1,2,3,4,5],[0,2,1,3,4,5],[0,1,3,2,4,5]]:
     var v=order.duplicate();v.append(1);check(C.solved(g,e,v),"Valid alternative assembly rejected")
   if e.mode=="seal":
    var v=C.initial(e);C.move(e,v,0);C.move(e,v,1);C.move(e,v,2);C.move(e,v,98)
    check(v[0]==0 and v[2]==0,"Three people crossed together")
    C.move(e,v,2);C.move(e,v,98);check(v.slice(0,3)==[3,1,2],"Pair crossing")
    C.move(e,v,2);check(v[3]==0,"Traveller selected on wrong seal side")
    C.move(e,v,99);check(v==[0,0,0,0],"Undo failed to restore position/time")
 print("CHAPTER4 STATE EXHAUSTION + PHYSICAL GATES + ALTERNATIVES + UNDO: ","FAIL" if failed else "PASS")
 quit(1 if failed else 0)
