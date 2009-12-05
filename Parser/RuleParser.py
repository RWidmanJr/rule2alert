# This code is published under GPL License Terms
#
# Descrpition: General Purpose rule parser
# Author: Pablo Rincon Crespo 5/12/2009
#


import re

class RuleUriContent:
    def __init__(self, uricontent):
        # check for negated uricontent option
        if uricontent[0] == "!":
            self.negated = True
            self.uricontent = uricontent[1:]
        else:
            self.negated = False
            self.uricontent = uricontent
        # Strip quotes.. "'s
        if self.uricontent[0] == '"':
            self.uricontent = self.uricontent[1:-1]

    def __str__(self):
        r = "RuleUriContent:\n"
        r = r + " - uricontent: "+ self.uricontent
        r = r + "\n" + " - negated: "+ str(self.negated)
        return r + "\n"

class RuleContent:
    def __init__(self, content):
        # check for negated content option
        if content[0] == "!":
            self.negated = True
            self.content = content[1:]
        else:
            self.negated = False
            self.content = content
        # Strip quotes.. "'s
        if self.content[0] == '"':
            self.content = self.content[1:-1]
        self.nocase = None
        self.rawbytes = None
        self.depth = None
        self.offset = None
        self.distance = None
        self.within = None
        self.http_client_body = None
        self.http_cookie = None
        self.http_header = None
        self.http_method = None
        self.http_uri = None
        self.fast_pattern = None

    def __str__(self):
        r = "RuleContent:\n"
        r = r + " - content: "+ self.content
        r = r + "\n" + " - negated: "+ str(self.negated)
        r = r + "\n" + " - nocase: "+ str(self.nocase)
        r = r + "\n" + " - rawbytes: "+ str(self.rawbytes)
        r = r + "\n" + " - depth: "+ str(self.depth)
        r = r + "\n" + " - offset: "+ str(self.offset)
        r = r + "\n" + " - distance: "+ str(self.distance)
        r = r + "\n" + " - within: "+ str(self.within)
        r = r + "\n" + " - http_client_body: "+ str(self.http_client_body)
        r = r + "\n" + " - http_cookie: "+ str(self.http_cookie)
        r = r + "\n" + " - http_header: "+ str(self.http_header)
        r = r + "\n" + " - http_method: "+ str(self.http_method)
        r = r + "\n" + " - http_uri: "+ str(self.http_uri)
        r = r + "\n" + " - fast_pattern: "+ str(self.fast_pattern) + "\n"
        return r

class Flow:
    def __init__(self, flowstr):
        self.stateless = False
        self.established = False
        self.from_client = False
        self.from_server = False
        self.to_client = False
        self.to_server = False
        self.no_stream= False
        self.stream_only= False

        p = re.compile(r'((?P<stateless>stateless)|(?P<established>established))')
        m = p.search(flowstr)

        if m and m.group("stateless") != None:
            self.stateless = True

        if m and m.group("established") != None:
            self.established = True

        #p = re.compile(r'((?P<stateless>stateless)|(?P<established>established))?')
        p = re.compile(r'((?P<to_server>to_server)|(?P<to_client>to_client))')
        m = p.search(flowstr)

        if m and m.group("to_client") != None:
            self.to_client = True

        if m and m.group("to_server") != None:
            self.to_server = True

        p = re.compile(r'((?P<from_client>from_client)|(?P<from_server>from_server))')
        m = p.search(flowstr)

        if m and m.group("from_client") != None:
            self.from_client = True

        if m and m.group("from_server") != None:
            self.from_server = True

        p = re.compile(r'((?P<stream_only>stream_only)|(?P<no_stream>no_stream))')
        m = p.search(flowstr)

        if m and m.group("stream_only") != None:
            self.stream_only = True

        if m and m.group("no_stream") != None:
            self.no_stream = True

    def __str__(self):
        r = "Flow: "
        f = False
        if self.stateless:
            if f:
                r = r + ", "
            r = r + "stateless"
            f=True
        if self.established:
            if f:
                r = r + ", "
            r = r + "established"
            f=True
        if self.from_client:
            if f:
                r = r + ", "
            r = r + "from_client"
            f=True
        if self.from_server:
            if f:
                r = r + ", "
            r = r + "from_server"
            f=True
        if self.to_client:
            if f:
                r = r + ", "
            r = r + "to_client"
            f=True
        if self.to_server:
            if f:
                r = r + ", "
            r = r + "to_server"
            f=True
        if self.no_stream:
            if f:
                r = r + ", "
            r = r + "no_stream"
            f=True
        if self.stream_only:
            if f:
                r = r + ", "
            r = r + "stream_only"
            f=True
        return r + "\n"

class Rule:
    raw=''
    type=''
    proto=''
    rawsources=''
    rawsrcports=''
    direc=''
    rawdestinations=''
    rawdesports=''
    rawoptions=''

    # We should implement all the options as attibutes, and this list should be empty in newer versions
    options=[]

    contents=[]
    uricontents=[]
    flow=None
    msg=''
    sid =''

    def __init__(self,rule):
        p = re.compile(r'^(?P<general>[^\(]+)\s*\((?P<rawoptions>.*)\)\s*$')
        m = p.search(rule)
        general = m.group("general")
        rawoptions = m.group("rawoptions")
    
        if general != None and rawoptions != None:
            pg = re.compile(r'(?P<type>[^\s]+)\s+(?P<proto>[^\s]+)\s+(?P<rawsources>[^\s]+)\s+(?P<rawsrcports>[^\s]+)\s+(?P<direc>[^\s]+)\s+(?P<rawdestinations>[^\s]+)\s+(?P<rawdesports>[^\s]+)\s*')
            m = pg.search(general)

            self.type = m.group('type')
            self.proto = m.group('proto')
            self.rawsources = m.group('rawsources')
            self.rawsrcports = m.group('rawsrcports')
            self.direc = m.group('direc')
            self.rawdestinations = m.group('rawdestinations')
            self.rawdesports = m.group('rawdesports')
            self.rawoptions = rawoptions
            
            po = re.compile(r'\s*([^;]+[^\\])\s*;')
            optlist = po.findall(rawoptions)
            self.options = []
            self.contents = []
            self.uricontents = []
            self.flow = None

            for i in optlist:
                pi = re.compile(r'^(?P<key>[^:]+)(\s*:\s*(?P<value>.*))?\s*$')
                mi = pi.search(i)
                k = mi.group("key")
                v = mi.group("value")
                if v == None:
                    v = True

                if k == "flow":
                    self.flow=Flow(v)
                    continue

                # Add as attributes the options that will not be "duplicated"
                # For options that can be duplicated/repeated do a list, like self.contents
                if k == "sid":
                    self.sid = v
                    continue

                if k == "msg":
                    self.msg=v
                    continue

                if k == "uricontent":
                    c = RuleUriContent(v)
                    self.uricontents.append(c)
                    continue

                if k == "content":
                    c = RuleContent(v)
                    self.contents.append(c)
                    continue

                # modifiers for contents
                if len(self.contents) > 0:
                    for clast in self.contents:
                        pass
                if k == "nocase":
                    clast.nocase = v
                    continue
                if k == "rawbytes":
                    clast.rawbytes = v
                    continue
                if k == "depth":
                    clast.depth = int(v)
                    continue
                if k == "offset":
                    clast.offset = int(v)
                    continue
                if k == "distance":
                    clast.distance = int(v)
                    continue
                if k == "within":
                    clast.within = int(v)
                    continue
                if k == "http_client body":
                    clast.http_client_body = v
                    continue
                if k == "http_cookie":
                    clast.http_cookie = v
                    continue
                if k == "http_header":
                    clast.http_header = v
                    continue
                if k == "http_method":
                    clast.http_method = v
                    continue
                if k == "http_uri":
                    clast.http_uri = v
                    continue
                if k == "fast_pattern":
                    clast.fast_pattern = v
                    continue

                self.options.append([k,v])
            
        else:
            print "Error loading rule " +str(rule)

    def __str__(self):
        r = "\nGeneral Fields:\n"
        r = r + "\n" + "type: "+ self.type
        r = r + "\n" + "proto: "+ self.proto
        r = r + "\n" + "rawsources: "+ self.rawsources
        r = r + "\n" + "sports: "+ self.rawsrcports
        r = r + "\n" + "direc: "+ self.direc
        r = r + "\n" + "dests: "+ self.rawdestinations
        r = r + "\n" + "dports: "+ self.rawdesports
        r = r + "\n" + "dports: "+ self.rawdesports

        r = r + "\n\nOption Fields:\n"
        r = r + "\n" + "msg: "+ self.msg
        r = r + "\n" + "sid: "+ self.sid

        if self.flow != None:
            r = r + "\n" + self.flow.__str__()

        for o in self.uricontents:
            r = r + "\n" + o.__str__() 

        for o in self.contents:
            r = r + "\n" + o.__str__() 

        r = r + "\n" + "Other Options:\n"
        for o in self.options:
            r = r + o[0] +":"+ str(o[1]) + ";\n"

        r = r + "\n" + "Options in raw: "+ self.rawoptions + "\n"
        return r

