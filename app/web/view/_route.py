from solo.web.route import Route
from solo.config import HOST

route = Route(host=HOST.replace(".", "\\."))

ROUTE_LIST = [route]
