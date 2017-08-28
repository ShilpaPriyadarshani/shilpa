'''
Author : Prabjot Singh

USAGE:
----------------------------------
from bugzilla_lib import bugzilla_lib
bug_api = bugzilla_lib("https://bugzilla-msys.qnap.com.tw/xmlrpc.cgi", "N03QtjSNZsCYTdqtXJD9QSirCwJBWuTCrIk5iYTJ")	
id=bug_api.create_bug("TestProduct", "unspecified", "TestComponent", "TEST BUG VIA python-bugzilla_test3", "This is comment #0 of an example bug created by the python-bugzilla.git examples/create.py script.", "Windows", "All", "shilpa.priyadarshani@msystechnologies.com")
----------------------------------
'''



import bugzilla

class bugzilla_lib():

	def __init__(self, url, api_key):
		#self.url = url
		#self.api_key = api_key
		self.bzapi = bugzilla.Bugzilla(url, api_key=api_key)
		print "Created bugzilla object"
		self.valid_status=["CONFIRMED", "IN_PROGRESS", "RESOLVED"]
		self.valid_resolutions = ["FIXED", "INVALId", "WONTFIX", "DUPLICATE", "WORKSFORME"]
		#pass

	def create_bug(self, product, version, component, summary, description, op_sys, platform, assigned_to):
		"""
		Function to create a new bug in bugzilla, all these parameters are mandatory
		Return : Returns bug id of the created bug / False in case of error
		"""
		try:
			createinfo = self.bzapi.build_createbug(
							product = product,
							version = version,
							component = component,
							summary = summary, 
							description = description, 
							op_sys = op_sys, 
							platform = platform,
							assigned_to = assigned_to
							)

			newbug = self.bzapi.createbug(createinfo)
			print "New bug created with bug id - '{}'".format(newbug.id)

			if newbug.id:
				return newbug.id
			else:
				print "Error while creating bug"
				return False
		except Exception as e:
			print "Exception occured while creating bug - {}".format(e)
			return False


	def add_comment(self, bug_id, comment):
		"""
		Function to add comment to a bug
		Return : Returns True or False
		"""
		try:
			update = self.bzapi.build_update(comment = comment)
			self.bzapi.update_bugs([bug_id], update)
			bug = self.bzapi.getbug(bug_id)
			bug.refresh()
			comments = bug.getcomments()

			if comment == comments[-1]["text"]:
				print "Comment added successfully"
				return True
			else:
				print "Failed to add comment"
				return False
		except Exception as e:
			print "Exception occured while adding comment to bug - {}".format(e)
			return False



	def update_status(self, bug_id, status, resolution=None):
		"""
		Function to change status of a bug
		Return : Returns True or False
		"""
		try:
			if status in self.valid_status:

				if status == "RESOLVED":
					if not resolution or (resolution not in self.valid_resolutions):
						print "Invalid resolution passed"
						
						return False



				if status == "RESOLVED":
					update = self.bzapi.build_update(status = status, resolution = resolution)
				else:
					update = self.bzapi.build_update(status = status)
				self.bzapi.update_bugs([bug_id], update)
				bug = self.bzapi.getbug(bug_id)
				bug.refresh()
				bug_status = bug.status

				if bug_status == status:
					print "Status changed successfully"
					return True
				else:
					print "Failed to update status"
					return False
			else:
				print "Invalid status state passed"
				return False
		except Exception as e:
			print "Exception occured while updating status of bug - {}".format(e)
			return False


	def get_all_bugs(self):
		"""
		Function to fetch all the bugs
		Return : Returns a list of dicts containing bug data
	
		----------------------------------------------
		[{'id': 1,
		  'status': 'CONFIRMED',
		  'summary': 'Snapshot : Snapshot schedule looses its scheduled time once schedule is disabled and enabled again.'},
		 {'id': 2,
		  'status': 'RESOLVED',
		  'summary': 'NFS : Client can not see the share and is not able to mount the share.'},
		 {'id': 3,
		  'status': 'CONFIRMED',
		  'summary': 'RAID: RAID 50 pool is getting created with 2 Disk'},
		 {'id': 4,
		  'status': 'CONFIRMED',
		  'summary': 'Share : Share is getting renamed/deleted while the IO is running from the client.'},
		 {'id': 5,
		  'status': 'CONFIRMED',
		  'summary': 'Hostlist: Adding a Host with Invalid IQN is getting succeeded.'},
		 {'id': 6,
		  'status': 'CONFIRMED',
		  'summary': 'Lun: Lun deletion succeeds when snapshot is already part of that same Lun'},
		 {'id': 7,
		  'status': 'CONFIRMED',
		  'summary': 'Hostlist: Adding a Host with Invalid Netaddress is getting succeeded.'},
		 {'id': 8,
		  'status': 'CONFIRMED',
		  'summary': 'Disk: Setting alarm_temp property for Disk smart config is accepting all values'},
		 {'id': 9,
		  'status': 'CONFIRMED',
		  'summary': 'Disk: Setting alarm_temp_scale property for Disk smart config is accepting all values'},
		 {'id': 10,
		  'status': 'CONFIRMED',
		  'summary': 'Ntpd: It accepts random values as interval for days and hours'},
		 {'id': 11,
		  'status': 'CONFIRMED',
		  'summary': 'Disk: Setting rapidtest_type property for Disk smart config is accepting all values'},
		 {'id': 12,
		  'status': 'CONFIRMED',
		  'summary': 'Disk: Setting rapid_weeklyday property for Disk smart config is accepting all values'},
		 {'id': 13,
		  'status': 'CONFIRMED',
		  'summary': 'Disk: Setting rapid_monthlyday  property for Disk smart config is accepting all values'},
		 {'id': 14,
		  'status': 'CONFIRMED',
		  'summary': 'Hostlist: Duplicate IQN entry for multiple host.'},
		 {'id': 15,
		  'status': 'RESOLVED',
		  'summary': 'Pool: Pool owner modify functionality is not working.'},
		 {'id': 16,
		  'status': 'CONFIRMED',
		  'summary': 'Disk: Setting rapid_hourmin property for Disk smart config is accepting all values'},
		 {'id': 17,
		  'status': 'RESOLVED',
		  'summary': 'Disk: Setting rapid_hourmin property for Disk smart config is accepting all values'},
		 {'id': 18,
		  'status': 'IN_PROGRESS',
		  'summary': 'Disk: Setting complete_weeklyday property for Disk smart config is accepting all values'},
		 {'id': 19,
		  'status': 'IN_PROGRESS',
		  'summary': 'Disk: Setting complete_monthlyday property for Disk smart config is accepting all values'},
		 {'id': 20,
		  'status': 'CONFIRMED',
		  'summary': 'Disk: Setting complete_hourmin property for Disk smart config is accepting all values'},
		 {'id': 21,
		  'status': 'CONFIRMED',
		  'summary': 'Target: Lun is not visible at initiator after making pool offline to online.'},
		 {'id': 22,
		  'status': 'CONFIRMED',
		  'summary': 'Target: Adding a Target with invalid IQN is getting succeeded.'},
		 {'id': 23,
		  'status': 'CONFIRMED',
		  'summary': 'Target: Lun is getting removed from target successfully, while IO is in progress.'},
		 {'id': 24,
		  'status': 'CONFIRMED',
		  'summary': 'new example summary 1503314537.15'},
		 {'id': 25, 'status': 'CONFIRMED', 'summary': 'TEST BUG VIA python-bugzilla'},
		 {'id': 26,
		  'status': 'CONFIRMED',
		  'summary': 'TEST BUG VIA python-bugzilla_test1'},
		 {'id': 27,
		  'status': 'CONFIRMED',
		  'summary': 'TEST BUG VIA python-bugzilla_test2'},
		 {'id': 28,
		  'status': 'CONFIRMED',
		  'summary': 'TEST BUG VIA python-bugzilla_test3'}
		]
		----------------------------------------------


		"""
		try:

			return_list =[]
			query = self.bzapi.build_query(include_fields=["summary", "id", "status"])
			bugs = self.bzapi.query(query)

			for bug in bugs:
				return_list.append({"id":bug.id, "summary":bug.summary, "status":bug.status})

			return return_list

		except Exception as e:
			print "Exception occured while fetching bugs - {}".format(e)
			return False
