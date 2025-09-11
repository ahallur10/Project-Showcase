class User:

	"""
		To initialise an instance of a User object the base requirements are the following:
		* walletid - A string value representative of a User instance's coinbase wallet id
			|- This string should theoretically be unique and serve as a username and ref to
				the instance's actual coinbase wallet
	"""
	def __init__(self, walletid): #is psw something to be kept in User? or db only aspect??
		self.__id = walletid 
		self.__numVids = 0
		self.__numGenres = 0
		self.__deposit = 0
		self.__withdrawl = 0
		self.__balance = self.__deposit - self.__withdrawl
		self.__activeTutorials = self.setInitMap()
		self.__completedTutorials = set() #set of Tutorial objects that are only to be added from a completed Tutorial

### GETTERS

	"""
		Getter for wallet id string
	"""
	def getWalletId(self):
		return self.__id
	
	"""
		Getter for number of videos user has watches total
	"""
	def getNumVids(self):
		return self.__numVids

	"""
		Getter for number of genres the user instance has watched
	"""
	def getNumGenres(self):
		return self.__numGenres

	"""
		Getter for current balance of user instances
	"""
	def getBalance(self):
		return self.__balance

	def getWalletId(self):
		return self.__id
	
	"""
		Getter for number of videos user has watches total
	"""
	def getNumVids(self):
		return self.__numVids

	"""
		Getter for number of genres the user instance has watched
	"""
	def getNumGenres(self):
		return self.__numGenres

	"""
		Getter for current balance of user instances
	"""
	def getBalance(self):
		return self.__balance

	"""
		Getter for all tutorial objects associated with instances of User which returns
		hashset for all tutorial accessed.
			Used set for this since with sets you can run functions like symmetric_difference,
			union, intersection, difference that can be useful when comparing users for stats
	"""
	def getTutorials(self):
		retval = set()
		for genre in self.__activeTutorials:
			for tutorial in self.__activeTutorials[genre]:
				retval.add(tutorial)
		return retval

	"""
		Gets the total number of active Tutorials for the User
	"""
	def numUserActive(self):
		total = 0
		for genre in self.__activeTutorials:
			total += len(self.__activeTutorials.get(genre))
		return total

	"""
		Returns an integer representing the ratio between the checks completed by the user for a
		particular Tutorial object and the total number of checks that the Tutorial object contains
			Ex: if the user has completed 3 checks out of 5 total checks the return val is 0.6
	"""
	def getUserCompletionRatio(self, TutorialObj):
		genre = TutorialObj.getGenre()
		totalLen = len(TutorialObj.getCompletion()[2:])
		if self.__activeTutorials.get(genre).get(TutorialObj) == bin(0):
			userLen = 0
		else:
			userLen = len(self.__activeTutorials.get(genre).get(TutorialObj)[2:])
		ratio = userLen / totalLen
		return ratio

	"""
		Getter for the Set of completed Tutorial objects
	"""
	def getUserCompleted(self):
		return self.__completedTutorials

	"""
		Gets the number of completed Tutorials
	"""
	def numUserCompleted(self):
		return len(self.__completedTutorials)

### SETTERS

	"""
		So when a User obj interacts with a tutorial obj, a check should
		be preformed so that the Tutorial object is set to the key of its
		corresponding genre. Genre values are ok to be hardcoded in since we have full
		control over the array of types they can encapsulate.
		The format of this nested map is going to be the following:
				map = {"Genre1" : {TutorialObject : binaryValue(starts at zero for every vid), ...}, ..etc}
	"""
	def setInitMap():
		hashMap = {"Art": dict(), "Sports": dict(), "Software": dict(), "Culinary": dict(), "Misc.": dict()}
		return hashMap



# Misc. functions

	"""
		Adds a new Tutorial object to nested diction if the genre of said object is a 
		valid option, else will raise err. Also initialises the begining value of added
		object to be zero; representing no checks done yet
	"""
	def addTutorial(self, TutorialObj):
		genre = TutorialObj.getGenre()
		if genre in self.__activeTutorials:
			self.__activeTutorials[genre][TutorialObj] = bin(0)
		else:
			raise ValueError("Not valid genre check string format or see valid genres")

	"""
		When a prompted check is passed, this will update binary values associated with Tutorial
		instance for the User. After the value is checked, Tutorial then checks itself versus the
		current value of User progress. If the Tutorial is deemed completed, the value is popped 
		from the map and is appended to the set of completed tutorials.
	"""
	def checkPassed(self, TutorialObj):
		genre = TutorialObj.getGenre()
		if self.__activeTutorials.get(genre).get(TutorialObj) == bin(0):
			val = 1
		else:
			val = int(self.__activeTutorials.get(genre).get(TutorialObj),2)
			val = (val << 1) | 1
		self.__activeTutorials[genre][TutorialObj] = bin(val)
		if TutorialObj.compCheck(self.__activeTutorials[genre][TutorialObj]) :
			self.__activeTutorials.get(genre).pop(TutorialObj)
			self.__completedTutorials.add(TutorialObj)
			return "Final Check passed, tutorial completed"
		else:
			return "Check Passed"
