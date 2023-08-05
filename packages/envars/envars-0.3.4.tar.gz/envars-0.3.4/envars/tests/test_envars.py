# Copyright (c) 2017 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""py.test for envars"""

from __future__ import print_function

from six import StringIO

import os

import envars.envars as envars


def test_dictvalue():
    """py.test for dictvalue"""
    data = (
        (dict(a=1, b=2), "a", "default", 1),
        # dct, key, defvalue, expected
        (dict(a=1, b=2), "c", "default", "default"),
        # dct, key, defvalue, expected
    )
    for dct, key, defvalue, expected in data:
        result = envars.dictvalue(dct, key, defvalue)
        assert result == expected


def test_getenvars():
    """py.test for getenvars"""
    data = (
        ("""a=1
            b=2""", 'a', "default", "1"),
        # envtxt, key, defvalue, expected
        ("""a=1
            b=2""", 'c', "default", "default"),
        # envtxt, key, defvalue, expected

        # test if envars cleans up comments
        ("""a=1 # comment
            b=2""", 'a', "default", "1"),
        # envtxt, key, defvalue, expected

        # test for blank line
        ("""a=1 # comment

            b=2""", 'a', "default", "1"),
        # envtxt, key, defvalue, expected
        # test for comment only line
        ("""a=1 # comment
            # comment only line
            b=2""", 'a', "default", "1"),
        # envtxt, key, defvalue, expected

    )
    for envtxt, key, defvalue, expected in data:
        fhandle = StringIO(envtxt)
        dct = envars.getenvars(fhandle=fhandle, defvalue=defvalue)
        result = dct[key]
        assert result == expected
    # test on os.environ -> as will happen on heroku
    os.environ['on_heroku'] = 'Yes'
    os.environ['another_heroku_value'] = 'avalue'
    dct = envars.getenvars(remoteKV=('on_heroku', 'Yes'))
    assert dct['another_heroku_value'] == 'avalue'
    # cleanup
    # os.environ.pop('on_heroku')
    # os.environ.pop('another_heroku_value')


def test_getenvarsfromenv(tmp_path):
    """pytest for a env fil"""
    data = (
    ("""a=1
        b=2""", 'a', "1"), # envtxt, key, expected
    )
    for envtxt, key, expected in data:
        envfile = tmp_path / ".env"
        # create the .env file
        with open(envfile, 'w') as fhandle:
            fhandle.write(envtxt)
        # test with the file handle - just because
        with open(envfile, 'r') as fhandle:        
            result = envars.getenvars(fhandle=fhandle)
        assert result[key] == expected
        # test with the .env file
        result = envars.getenvars(defaultfilename=envfile)
        assert result[key] == expected
        # test with nonexistent file
        nofile = tmp_path / ".nofile"
        result = envars.getenvars(defaultfilename=nofile)
        assert result == {}
        