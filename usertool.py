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
parser.add_argument('-link', '--server-link', default='127.0.0.1')
parser.add_argument('-port', '--server-port', default=27017)

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()
user_account = caccount(user="root", group="root")
my_storage = cstorage(user_account, namespace='object', logging_level=logging.DEBUG, mongo_host=args.server_link)

if (args.list_users):
	records = my_storage.find({'crecord_type':'account'},account=user_account)
	counter = 0
	for record in records:
		counter += 1 
		record_dict = record.dump()
		print "User: %s" % (record_dict['user'])
		print "Mail: %s" % (record_dict['mail'])
		print "Pass: %s" % (record_dict['shadowpasswd'])
		print ""
	print "DEBUG: total accounts = %s" % counter

if (args.add_user):
	print "entering add_user case"
	if not args.user_name:
		print "args.user_name is None"
		sys.exit(1)
	elif not args.user_pass:
		print "args.user_pass is None"
		sys.exit(1)
	elif not args.user_mail:
		print "args.user_mail is None"
		sys.exit(1)
	else:
		m = hashlib.sha1()
		m.update(args.user_pass)
		cpassword = m.hexdigest()
		time_stamp = int(time.time())
		post = caccount(user=args.user_name, group="capensis", mail=args.user_mail, )
		my_record = caccount(post, storage=my_storage)
		my_storage.put(my_record)
		output = my_storage.find({'crecord_type':'account'},account=user_account)
		print "DEBUG: len output = %s" % (len(output))
	
if (args.delete_user):
	if not args.user_name:
		print "args.user_name is None"
		sys.exit(1)
	else:
		my_record = my_storage.find({'user' : args.user_name})
		my_storage.remove(my_record, account=user_account)
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
			my_account = caccount(user=args.user_name)
			my_account.passwd(args.user_pass)
			print ("DEBUG: \n===== \n \n"), my_account.cat()
			my_storage.put(my_account)



