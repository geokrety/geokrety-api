# Contributing to GeoKrety Api

:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

# Contact us

You can find us on IRC at channel #geokrety.

# Running the Tests

WARNING NEVER LAUNCH THE TESTS ON A PRODUCTION SERVER, IT WILL DESTROY ALL YOUR DATA!

Before submitting your pull request, it is recommended to launch the Unit Tests and documentation validation.

## Unit Tests

### Launch all tests:

```
nosetests tests/unittests/ --verbose
```

### Launch tests on a specific file:
```
nosetests --verbose --nologcapture tests/unittests/api/test_geokrety_create.py
```

### Launch tests on a specific file and specific function:
```
nosetests --verbose --nologcapture tests/unittests/api/test_geokrety_create.py:TestGeokretCreate.test_owner_enforced_to_current_user
```

### Launch tests automatically on file change:

```
nosetests --verbose --with-watcher --filetype .py --nologcapture tests/
```

Alternatively, you can use `inotify`. You need to install `inotify-tools` (On Ubuntu: `sudo apt install inotify-tools`)
```
inotifywait -r -m -e close_write --exclude '\.pyc$' . | while read path _ file; do nosetests tests/unittests/api/test_geokret.py --verbose; done
```

### Check code coverage
Please do your best to reach/stay at 100%!
```
nosetests --verbose --nologcapture  --with-coverage --cover-package=app --cover-inclusive tests/unittests/
```

## Validating documentation

For easier management, we have split the Api Blueprint in different files. You can combine them to the root of your repository checkout and as we configured git to ignore this file it won't be added to the repository. If you prefer to recombine the whole file somewhere else, please ensure to not commit the file to the repository.

```
cat docs/*.apib > apiary.apib && dredd
```

# Recommendations

* Please rebase your Pull Requests uppon master.
*  Avoid "fixup" commits.
