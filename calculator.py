"""
A wsgi calculator which supports these operations between two numbers:

  * Addition
  * Subtractions
  * Multiplication
  * Division


Examples of use:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => Instructions...
```
"""

import re
import traceback

def instructions():
    page = '''
<h1>Instructions</h1>
<h2>Put add, subtract, multiply, divide with two numbers following them to calculate.</h2>
<h3>Examples:</h3>
<ul>
  <li>http://localhost:8080/multiply/3/5   => 15</li>
  <li>http://localhost:8080/add/23/42      => 65</li>
  <li>http://localhost:8080/subtract/23/42 => -19</li>
  <li>http://localhost:8080/divide/22/11   => 2</li>
</ul>
    '''
    return page

def add(*args):
    """ Returns a STRING with the sum of the arguments """
    _sum = int(args[0]) + int(args[1])
    page = '<h1>{} + {} = {}</h1>'.format(args[0], args[1], _sum)

    return page

def subtract(*args):
    """ Returns a STRING with the difference of the arguments """
    subt = int(args[0]) - int(args[1])
    page = '<h1>{} - {} = {}</h1>'.format(args[0], args[1], subt)

    return page

def multiply(*args):
    """ Returns a STRING with the product of the arguments """
    mult = int(args[0]) * int(args[1])
    page = '<h1>{} * {} = {}</h1>'.format(args[0], args[1], mult)

    return page

def divide(*args):
    """ Returns a STRING with the quotient of the arguments """
    if int(args[1]) == 0:
      raise ZeroDivisionError

    div = int(args[0]) / int(args[1])
    page = '<h1>{} / {} = {}</h1>'.format(args[0], args[1], div)

    return page

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    funcs = {'':instructions, 'add': add, 'subtract': subtract,
     'multiply': multiply, 'divide': divide}

    path = path.strip('/').split('/')
    func_name = path[0]
    args = path[1:]

    try:
      func = funcs[func_name]
    except KeyError:
      raise NameError

    return func, args

def application(environ, start_response):
    """
    Run the wsgi application
    """
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = '200 OK'
    except NameError:
        status = "404 Not Found"
        body = "<h1> Not Found</h1>"
    except ZeroDivisionError:
        status = "400 Bad Request"
        body = "<h1> Cannot Divide by Zero</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
