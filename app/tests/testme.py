from nose.tools import eq_
from runme import encrypt
from runme import write_user, read_users


import random
import sqlite3 as db
import subprocess

def test_pwd():
    for r in range(0, 100):
        # Generate random password
        pwd = "".join([chr(random.randint(33, 122)) for c in range(0, 31)])
        key = "".join([chr(random.randint(33, 122)) for c in range(0, 31)])

        assert(pwd == encrypt(key, encrypt(key, pwd, True)))

def test_db_write():
    write_user('testUser1', 'imJust!aTestUsr*')
    conn = db.connect('sample.db')
    q = conn.execute('SELECT * FROM usrdb WHERE user="testUser1"')
    b = q.fetchall()
    conn.commit()
    conn.close()
    assert (b[0][0] == 'testUser1')

def test_db_write2():
    assert(-1 == write_user('testUser1', 'imJust!aTestUsr*'))

def test_db_read():
    assert('testUser1' in zip(*read_users())[0])

def test_clean():
    assert(0 == subprocess.call(['rm', 'sample.db']))
