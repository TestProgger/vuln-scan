import netifaces


gateways = netifaces.gateways()
DEFAULT_GATEWAY = None
INTERFACE_NAME = None
CURRENT_HOST_IP = None
CURRENT_HOST_MAC = None

if "default" in gateways:
    DEFAULT_GATEWAY, INTERFACE_NAME = gateways["default"][netifaces.AF_INET]

interfaces = netifaces.interfaces()
for interface in interfaces:
    _startswith_gateway = ".".join(DEFAULT_GATEWAY.split('.')[:3])
    addrs = netifaces.ifaddresses(str(interface))
    try:
        af_inet = addrs[netifaces.AF_INET]
        af_link = addrs[netifaces.AF_LINK]

        if af_inet[0]['addr'].startswith(_startswith_gateway):
            CURRENT_HOST_IP = af_inet[0]['addr']
            CURRENT_HOST_MAC = af_link[0]['addr'].upper()
    except:
        pass