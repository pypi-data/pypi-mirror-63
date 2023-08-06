import json
import re
from functools import partial
from .singleton import Singleton
from .route_parser import parse_route_for_path

class RouteHolder(metaclass=Singleton):
  def __init__(self):
    self._routes = {}

  def _hoist_request(self, route, event, *, respondent):
    params = {}
    if event['queryStringParameters']:
      params = {**params, **event['queryStringParameters']}
    if event['multiValueQueryStringParameters']:
      params = {**params, **event['multiValueQueryStringParameters']}
    params = {**params, **event['pathParameters']}
    if event['body']:
      params['raw_body'] = event['body']
      params['parsed_body'] = {}
      if re.search('json', event['headers'].get('content-type', ''), re.IGNORECASE):
        try:
          params['parsed_body'] = json.loads(event['body'])
        except json.JSONDecodeError:
          pass

    params = {**params, **parse_route_for_path(route['route'], event['pathParameters'].get('proxy', ''))}
    return route['function'](params, event=event, respondent=respondent)

  def _evaluate_route(self, path, http_method, route):
    if route['http_method'] != 'ANY' and route['http_method'] != http_method:
      return False
    
    if parse_route_for_path(route['route'], path) is None:
      return False
    return True

  def find_best_route(self, path, http_method):
    path_evaluator = partial(self._evaluate_route, path, http_method)
    valid_routes = sorted(filter(path_evaluator, self.routes), key=lambda x: -x['route'].count('/'))
    if valid_routes:
      return partial(self._hoist_request, valid_routes[0])
    return None

  def add_route_partial(self, func, route=None, http_method=None):
    key = '{}-{}'.format(func.__module__, func.__name__)
    if not key in self._routes:
      self._routes[key] = {'http_method': 'ANY'}

    self._routes[key]['function'] = func
    if route is not None:
      self._routes[key]['route'] = route
    if http_method is not None:
      self._routes[key]['http_method'] = http_method

  @property
  def routes(self):
    return self._routes.values()