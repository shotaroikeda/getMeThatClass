#!/usr/bin/python
import sqlite3
import os.path

DELETE_ME_SALT = 'hL\\x7f<Q0>W?5\\x81\\x80|G:G@hQUT9M_cZTn{Zqc={>^_RNN6oqvIz\\x7fjH_'

def encrypt(key, passw, dec=False):
    """Encrypts a password based on the key"""
    key_list = list(key)
    key_len = len(key)
    enc = []
    for i, c in enumerate(list(passw)):
        enc.append(iter_keyws(c, key_list[i % key_len], dec))

    return "".join(enc)

def iter_keyws(charlike, shift, reverse=False):
    """
    Make sure that the password becomes iterable.
    Basic acceptable ranges:

    [33, 122]
    """

    if reverse:
        result_c = 59 + ord(charlike) - ord(shift)
        while result_c <= 32:
            result_c += 91

        if result_c > 123:
            result_c = (result_c - 32) % 91 + 32

        return chr(result_c)
    else:
        result_c = ((ord(charlike) + ord(shift)) % 91) + 32
        return chr(result_c)

def write_user(user, passw):
    if os.path.isfile('sample.db'):
        conn = sqlite3.connect('sample.db')

        # Check if the username was already created
        query = conn.execute("SELECT user FROM usrdb WHERE user=?", (user,))

        if len(query.fetchall() > 0):
            conn.close()
            return -1  # User already exists

        conn.execute("INSERT INTO usrdb VALUES(?, ?)", (user, encrypt(DELETE_ME_SALT, passw)))
        conn.commit()
        conn.close()

    else:
        conn = sqlite3.connect('sample.db')
        conn.execute("CREATE TABLE usrdb(user TEXT, passw TEXT)")
        conn.execute("INSERT INTO usrdb VALUES(?, ?)", (user, encrypt(DELETE_ME_SALT, passw)))
        conn.commit()
        conn.close()

    return 0  # Everything is good

def read_users():
    conn = sqlite3.connect('sample.db')
    query = conn.execute('SELECT * FROM usrdb')

    t = query.fetchall()

    conn.close()

    return t

def test_cases():
    password = "heilo_world"
    keyword_linear = "aaaaaaa"
    keyword_word = "superboiz"

    assert(password == encrypt(keyword_linear,
                               encrypt(keyword_linear, password),
                               True))
    assert(password == encrypt(keyword_word,
                               encrypt(keyword_word, password),
                               True))

def r_test():
    import random
    for r in range(0, 100000):
        # Generate random password
        pwd = "".join([chr(random.randint(33, 122)) for c in range(0, 31)])
        key = "".join([chr(random.randint(33, 122)) for c in range(0, 31)])

        try:
            assert(pwd == encrypt(key, encrypt(key, pwd), True))
        except AssertionError:
            print "ERROR! Failed test case:"
            print "Password: %s" % (pwd)
            print "Key: %s" % (key)
            print "Original: "
            for c1, c2 in zip(list(pwd), list(encrypt(key, encrypt(key, pwd), True))):
                if c1 is not c2:
                    print "Different chars: %c, %c" % (c1, c2)
            pass

    print "All tests pass!"
