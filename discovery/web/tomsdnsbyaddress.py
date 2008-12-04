#!/usr/bin/env python
#
#   hostmap
#
#   Author:
#    Alessandro `jekil` Tanasi <alessandro@tanasi.it>
#
#   License:
#    This program is private software; you can't redistribute it and/or modify
#    it. All copies, included printed copies, are unauthorized.
#    
#    If you need a copy of this software you must ask for it writing an
#    email to Alessandro `jekil` Tanasi <alessandro@tanasi.it>



import re
from twisted.web import client
from lib.output.outputDeflector import log



class tomsdnsbyaddress:
    """ 
    Check against tomsdns
    @author: Alessandro Tanasi
    @license: Private software
    @contact: alessandro@tanasi.it
    """



    def require(self):
        """
        Sets plugin requirements
        """
        
        # Possible values are:
        # ip
        # domain
        # nameserver
        # hostname
        return "ip"



    def run(self, hd, ip):
        """
        Query Tomdns using dork ip: to ge a list of domains
        """
    
        self.job = "%s-%s" % (__name__, ip)
        hd.job(self.job, "starting")
        
        # Compose url
        url = "http://www.tomdns.net/get_hostonip.php?target=%s" % ip
        
        # Search
        query = client.getPage(url)
        query.addCallback(self.__callSuccess, hd)
        query.addErrback(self.__callFailure, hd)
        
        hd.job(self.job, "waiting")
    


    def __callFailure(self, failure, hd):
        """
        If a Tomdns search run fails
        """
        
        # failure.printTraceback()
        
        hd.job(self.job, "failure")


    def __callSuccess(self, success, hd):
        """
        If a Tomdns run success
        """
        
        # TODO: test this and redo the parsing regexp
        # Regexp to catch fqdn
        regexp = "-->([\d\w\.-_\r\n]+)<"
        # Cast object, paranoid mode
        page = str(success)

        # Grep
        results = re.findall(regexp, page, re.M)[0]
        results = re.split("\n", results)[1:-2]
        
        # Add new found hosts
        for host in set(results):
            hd.notifyHost(host)
            log.debug("Plugin %s added result: %s" % (__name__, host))
        
        hd.job(self.job, "done")
