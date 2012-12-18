bitly-assumptionator
====================

Page demoing some bitly API stuff.

To install this, try (preferably in a virtualenv):

```
  python setup.py develop
```

or:

```  
  pip install -e .
```

You'll need a bitly API token. To generate one, do this once
as the user that will run your web server:

```
  python assumptionator/bitly_api.py
```

This will prompt you for a username / password and store your API token
in ~/.bitly_api_tokens.




