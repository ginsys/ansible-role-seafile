#!/usr/bin/env python

#coding: UTF-8

# {{ ansible_managed }}

import check_init_admin
import os
import sys
import  subprocess

def main():
    subprocess.call(["{{ seafile_latest_dir }}/seafile.sh", "start"])
    if check_init_admin.need_create_admin():
        check_init_admin.create_admin('{{ seafile_seahub_admin_email }}', '{{ seafile_seahub_admin_password }}')
    else:
        print "changed=false"
    subprocess.call(["{{ seafile_latest_dir }}/seafile.sh", "stop"])

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print '\n\n\n'
        print 'Aborted.'
        print
        sys.exit(1)
    except Exception, e:
        print
        print 'Error happened during creating seafile admin:'
        print e
        print
        sys.exit(1)
