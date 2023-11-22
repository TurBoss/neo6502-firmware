# ***************************************************************************************
# ***************************************************************************************
#
#      Name :      makedispatch.py
#      Authors :   Paul Robson (paul@robsons.org.uk)
#      Date :      22nd November 2023
#      Reviewed :  No
#      Purpose :   Build dispatch files.
#
# ***************************************************************************************
# ***************************************************************************************

import sys

# ***************************************************************************************
#
#						Represents function and associated code
#
# ***************************************************************************************

class Function(object):
	def __init__(self,funcID,funcName = None):
		self.funcID = funcID
		self.lines = []
		self.funcName = funcName if funcName is not None else "Function "+str(funcID)
	#
	def addCode(self,codeLine):
		self.lines.append(codeLine.rstrip())
	#
	def getID(self):
		return self.funcID
	#
	def render(self):
		print("\t\t\tcase {0}:".format(self.funcID))
		for l in self.lines:
			print("\t\t\t\t"+l)
		print("\t\t\t\tbreak;")

# ***************************************************************************************
#
#							Represents group of functions
#
# ***************************************************************************************

class Group(object):
	def __init__(self,groupID,groupName = None):
		self.groupID = groupID
		self.groupName = groupName if groupName is not None else "Group "+str(groupID)
		self.functions = {}
	#
	def getID(self):
		return self.groupID
	#
	def addFunction(self,func):
		assert func.getID() not in self.functions
		self.functions[func.getID()] = func
	#
	def render(self):
		print("\tcase {0}:".format(self.groupID))
		print("\t\tswitch (*DFUNCTION) {")
		funcs = [x for x in self.functions.keys()]
		funcs.sort()
		for f in funcs:
			self.functions[f].render()
		print("\t\t}")
		print("\t\tbreak;")

# ***************************************************************************************
#
# 				Represents a Dispatch API, a collection of groups
#
# ***************************************************************************************

class DispatchAPI(object):
	def __init__(self):
		self.currentFunction = None 
		self.currentGroup = None
		self.groups = {}
	#
	def addGroup(self,group):	
		assert group.getID() not in self.groups 
		self.currentGroup = group
		self.groups[group.getID()] = group 
		self.currentFunction = None 
	#
	def addFunction(self,func):
		assert self.currentGroup is not None 
		self.currentFunction = func
		self.currentGroup.addFunction(func)
	#
	def addCode(self,codeLine):
		assert self.currentFunction is not None 
		self.currentFunction.addCode(codeLine)
	#
	def processLine(self,s):
		s = s  if s.find("//") < 0 else s[:s.find("//")]
		s = s.strip()
		if s != "":			
			if s.startswith("group"):
				self.addGroup(Group(int(s[5:].strip())))
			elif s.startswith("function"):
				self.addFunction(Function(int(s[8:].strip())))
			else:
				self.addCode(s)
		#
	def render(self):
		print("//\n//\tThis file is automatically generated\n//")
		print("switch (*DCOMMAND) {")
		groups = [x for x in self.groups.keys()]
		groups.sort()
		for k in groups:
			self.groups[k].render()
		print("}")

api = DispatchAPI()
for f in sys.argv[1:]:
	for l in open(f).readlines():
		api.processLine(l)
api.render()