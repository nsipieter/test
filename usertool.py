#!/usr/bin/env python
import sys, hashlib, getpass, time, argparse, logging
from caccount import caccount, caccount_get, caccount_getall
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

def user_exist(cstorage, user):
	try:
		xyz = caccount_get(cstorage,user)
	except:
		xyz = None
	if (args.debug_output):
		print ("DEBUG: xyz = %s \n" %xyz)	
	return xyz

if (args.list_users):
	bleh = caccount_getall(my_storage)
	counter = 0
	for i in bleh:
		counter +=1
		print i.cat()
		print " + shadowpasswd:\t",i.shadowpasswd, "\n"
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
		my_user=user_exist(my_storage, args.user_name)
		if (my_user is None):	
			my_storage.put(my_account)
			print ("user %s added \n" %(args.user_name))
		else:
			print ("user already exist \n")
			sys.exit(1)
	
if (args.delete_user):
	if not args.user_name:
		print "args.user_name is None"
		sys.exit(1)
	else:
		my_user=user_exist(my_storage, args.user_name)
		if (my_user is not None):	
			my_storage.remove(my_user, account=whoami)
			print ("user %s deleted \n" %(args.user_name))
		else:
			print ("user doesn't exist \n")
			sys.exit(1)

if (args.user_chpass):
		if not args.user_name:
			print "args.user_name is None"
			sys.exit(1)
		elif not args.user_pass:
			print "args.user_pass is None"
			sys.exit(1)
		else:
			my_user=user_exist(my_storage, args.user_name)
			if (my_user is not None):
				my_user.passwd(args.user_pass)
				my_storage.put(my_user)
			else:
				print ("user doesn't exist \n")
				sys.exit(1)



