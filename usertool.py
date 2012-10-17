#!/usr/bin/env python
import sys, hashlib, getpass, time, argparse
from caccount import caccount
from cstorage import cstorage
from pymongo import Connection
from crecord import crecord
import logging

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

connection = Connection(args.server_link, args.server_port)
db = connection.canopsis
collection = db.object

user_account = caccount(user="root", group="root")
my_storage = cstorage(user_account, namespace='object', logging_level=logging.DEBUG, mongo_host=args.server_link)


if (args.list_users):

# current: user_account.cat utilise la couche d'abstraction
	for i in collection.find():
		if i.get('crecord_type', False) == 'account':
			user_account = caccount(user=i['user'], group="capensis")
			user_account.cat()


	records = my_storage.find({'crecord_type':'account'},account=user_account)
	for record in records:
		record_dict = record.dump()
		print "User: %s" % (record_dict['user'])
		print "Mail: %s" % (record_dict['mail'])
		print "Pass: %s" % (record_dict['shadowpasswd'])
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
		"""
		post = {u'aaa_access_owner': [u'r', u'w'], u'aaa_group': u'group.CPS_'+ args.user_name, 
		u'aaa_admin_group': u'group.CPS_account_admin', u'children': [], 
		u'firstname': u'maxwell', u'shadowpasswd': cpassword, u'aaa_access_unauth': [], 
		u'crecord_type': u'account', u'mail': args.user_mail, u'crecord_creation_time': time_stamp,
		u'crecord_write_time': time_stamp, u'enable': True,	u'aaa_access_group': [u'r'], 
		u'parent': [], u'lastname': args.user_name,
		u'authkey': u'5b7d1ad4384332a0bd0030a4f82fc667989fe73d43b247a2f0dbce40', 
		u'user': args.user_name, u'groups': [], u'crecord_name': args.user_name, 
		u'aaa_owner': u'account.'+ args.user_name, u'aaa_access_other': [], u'_id': u'account.'+args.user_name}
		#collection.insert(post)
		"""
		post = caccount(user=args.user_name, group="capensis", mail=args.user_mail, )
		my_record = caccount(post, storage=my_storage)
		my_storage.put(my_record, namespace='object')
		output = my_storage.find({'crecord_type':'account'},account=user_account)
		print "len output = %s" % (len(output))

	
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
			m = hashlib.sha1()
			m.update(args.user_pass)			
			collection.update({'crecord_type': 'account', 'user' : args.user_name}, {'$set': {'shadowpasswd' : m.hexdigest()}})
	







