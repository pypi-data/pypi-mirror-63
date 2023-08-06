These testfiles are designed to test features of the various classes.  To run these tests, you need the [nosetesting package](http://nose.readthedocs.io/en/latest/).

The simplest way to invoke the tests is to execute

    nosetests3 sosia/tests/ --verbose

in the command line from within the sosia repo.

During the tests, files from the Scopus database are downloaded and cached in the usual way.  Hence, tests make use of your API Key and require a valid connection.
