extends RefCounted
# French remains the canonical source, including journal entries in older saves.
# Longest-first matching also translates composed entries without touching IDs.
const SETTINGS="user://language.cfg"
var language="fr"
var english={}
var matcher=RegEx.new()
var cache={}

func _init():
	english=JSON.parse_string(FileAccess.get_file_as_string("res://data/en.json"))
	# Register authored endings before compiling composed-text matching (HUD/journal).
	var endings=JSON.parse_string(FileAccess.get_file_as_string("res://data/endings.json"))
	for entry in endings.values():
		for field in ["title","text","action","objective","success"]:
			if entry.has(field):english[entry[field][0]]=entry[field][1]
	var subject=JSON.parse_string(FileAccess.get_file_as_string("res://data/subject16.json"))
	english.merge(subject.ui,true)
	for entry in subject.chapters.values():
		for field in ["name","collectible"]:english[entry[field][0]]=entry[field][1]
		for i in range(1,11):english[entry.collectible[0]+" · K%02d"%i]=entry.collectible[1]+" · K%02d"%i
		for pair in entry.archives:english[pair[0]]=pair[1]
	for list_v in subject.reactions.values():
		for pair in list_v:english[pair[0]]=pair[1]
	var keys=english.keys().filter(func(value): return not value.strip_edges().is_empty())
	keys.sort_custom(func(a,b): return a.length()>b.length())
	var patterns=PackedStringArray()
	for source in keys:
		var escaped=""
		for ch in source:
			if ch in "\\.^$|?*+()[]{}": escaped+="\\"
			escaped+=ch
		patterns.append(escaped)
	matcher.compile("|".join(patterns))
	load_preference()

func load_preference():
	var config=ConfigFile.new()
	if config.load(SETTINGS)==OK:
		var saved=config.get_value("interface","language","fr")
		if saved in ["fr","en"]: language=saved

func choose(value,persist=true):
	if value not in ["fr","en"]: return
	language=value
	if persist:
		var config=ConfigFile.new()
		config.set_value("interface","language",language)
		config.save(SETTINGS)

func translate(source):
	if language=="fr" or source.is_empty(): return source
	if english.has(source): return english[source]
	if cache.has(source): return cache[source]
	var result=""
	var cursor=0
	for found in matcher.search_all(source):
		result+=source.substr(cursor,found.get_start()-cursor)+english[found.get_string()]
		cursor=found.get_end()
	result+=source.substr(cursor)
	cache[source]=result
	return result
