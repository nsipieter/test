#!/usr/bin/env python
import sys, hashlib, getpass, time, argparse, logging
from caccount import caccount
from cstorage import cstorage
from pymongo import Connection
from crecord import crecord

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    )

parser = argparse.ArgumentParser()
parser.add_argument('-list', '--list-users')
parser.add_argument('-add',  '--add-user')
parser.add_argument('-del',  '--delete-user')
parser.add_argument('-chpa', '--user-chpass')
parser.add_argument('-user', '--user-name')
parser.add_argument('-pass', '--user-pass')
parser.add_argument('-mail', '--user-mail')
parser.add_argument('-fnam', '--first-name')
parser.add_argument('-lnam', '--last-name')
parser.add_argument('-link', '--server-link', default='127.0.0.1')
parser.add_argument('-port', '--server-port', default=27017)
parser.add_argument('-debg', '--debug-output')

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()
if (args.debug_output):
	verbosity = logging.DEBUG
else:
	verbosity = logging.ERROR
whoami = caccount(user="root", group="root")
my_storage = cstorage(whoami, namespace='object', logging_level=verbosity, mongo_host=args.server_link)

if (args.list_users):
	records = my_storage.find({'crecord_type':'account'},account=whoami)
	counter = 0
	bleh()
	for record in records:
		#record.cat()
		counter += 1 
		record_dict = record.dump()
		print "lastname: %s" % (record_dict['lastname'])
		print "firstname: %s" % (record_dict['firstname'])
		print "User: %s" % (record_dict['user'])
		print "Mail: %s" % (record_dict['mail'])
		print "Pass: %s" % (record_dict['shadowpasswd'])
		print "groups: %s" % (record_dict['groups'])
		print "authkey: %s" % (record_dict['authkey'])
		print ""

	if (args.debug_output):
		print "DEBUG: total accounts = %s" % counter

if (args.add_user):
	if not args.user_name:
		print "args.user_name is None"
		sys.exit(1)
	elif not args.user_pass:
		print "args.user_pass is None"
		sys.exit(1)
	elif not args.first_name:
		print "args.first_name is None"
		sys.exit(1)
	elif not args.last_name:
		print "args.last_name is None"
		sys.exit(1)	
	elif not args.user_mail:
		print "args.user_mail is None"
		sys.exit(1)
	else:
		my_account = caccount(firstname=args.first_name, lastname=args.last_name, user=args.user_name, group="capensis", mail=args.user_mail)
		my_account.passwd(args.user_pass)
		# my_record = caccount(my_account, storage=my_storage)
		# verify if account doesn't already exist
		if (my_storage.count({'user' : args.user_name, 'lastname': args.last_name, 'crecord_type':'account'})):
			print ("user already exist \n")
			sys.exit(1)

		my_storage.put(my_account)		
		if (args.debug_output):
			output = my_storage.count({'crecord_type':'account'},account=whoami)
			print "DEBUG: len output = %s" % (len(output))
	
if (args.delete_user):
	if not args.user_name:
		print "args.user_name is None"
		sys.exit(1)
	else:
		try:
			my_record = my_storage.find({'user' : args.user_name})
		except:
			print "user doesn't exist\n"
			sys.exit(1)
		my_storage.remove(my_record, account=whoami)
		if (args.debug_output):
			print "DEBUG mrecord = ", my_record
			print "DEBUG mstorage = ",my_storage

if (args.user_chpass):
		if not args.user_name:
			print "args.user_name is None"
			sys.exit(1)
		elif not args.user_pass:
			print "args.user_pass is None"
			sys.exit(1)
		else:
			try:
				user_accounts = my_storage.find({'crecord_type':'account', 'user' : args.user_name},account=whoami) # get crecord_type
				
				# utiliser get ou plutot find_one
				# trasformer ce crecord en caccount my_account = caccount(record=user_accounts)
				# reste a faire caccount.showdpasswd



			except:
				print "user doesn't exist"
				sys.exit(1)
			
			#backup user data before modifying anything
			for each_entry in user_accounts:
				user_dict 	= each_entry.dump()
				user_fname	= user_dict['firstname']
				user_lname	= user_dict['lastname']
				#user_group 	= user_dict['group']
				user_groups = user_dict['groups']
				user_mail 	= user_dict['mail']
			my_account = caccount(user=args.user_name, mail=user_mail, firstname=user_fname, lastname=user_lname, groups=user_groups)
			my_account.passwd(args.user_pass)
			my_storage.put(my_account)
			if (args.debug_output):
				print ("DEBUG: \n===== \n \n"), my_account.cat()
			
def bleh():
	pass


