#!/usr/bin/env python
import sys, hashlib, getpass, time, argparse
from pymongo import Connection

connection = Connection('172.16.49.130',27017)
db = connection.canopsis
collection = db.object

parser = argparse.ArgumentParser()

parser.add_argument('-l', '--list-users')
parser.add_argument('-a', '--add-user')
parser.add_argument('-d', '--delete-user')
parser.add_argument('-c', '--user-chpass')
parser.add_argument('-u', '--user-name')
parser.add_argument('-p', '--user-pass')
parser.add_argument('-m', '--user-mail')

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()

if (args.list_users):
	print "list_user is true"
	for i in collection.find():
		if i.get('crecord_type', False) == 'account':
			my_name  = i['user']
			my_pass  = i['shadowpasswd']
			my_mail  = i['mail']
			print "User: %s" % (my_name)
			print "Mail: %s" % (my_mail)
			print "Pass: %s" % (my_pass)
			print ""

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
		post = {u'aaa_access_owner': [u'r', u'w'], u'aaa_group': u'group.CPS_'+ args.user_name, 
		u'aaa_admin_group': u'group.CPS_account_admin', u'children': [], 
		u'firstname': u'maxwell', u'shadowpasswd': cpassword, u'aaa_access_unauth': [], 
		u'crecord_type': u'account', u'mail': args.user_mail, u'crecord_creation_time': time_stamp,
		u'crecord_write_time': time_stamp, u'enable': True,	u'aaa_access_group': [u'r'], 
		u'parent': [], u'lastname': args.user_name,
		u'authkey': u'5b7d1ad4384332a0bd0030a4f82fc667989fe73d43b247a2f0dbce40', 
		u'user': args.user_name, u'groups': [], u'crecord_name': args.user_name, 
		u'aaa_owner': u'account.'+ args.user_name, u'aaa_access_other': [], u'_id': u'account.'+args.user_name}
		collection.insert(post)
	
if (args.delete_user):
	if not args.user_name:
		print "args.user_name is None"
		sys.exit(1)
	else:
		collection.remove({'_id' : 'account.'+args.user_name})

if (args.user_chpass):
		if not args.user_name:
			print "args.user_name is None"
			sys.exit(1)
		elif not args.user_pass:
			print "args.user_pass is None"
			sys.exit(1)
		else:
			m = hashlib.sha1()
			m.update(args.user_pass)			
			collection.update({'crecord_type': 'account', 'user' : args.user_name}, {'$set': {'shadowpasswd' : m.hexdigest()}})








