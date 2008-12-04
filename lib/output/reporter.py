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



from lib.output.outputDeflector import log
from lib.core.configuration import conf



class Report():
    """
    Report results
    @license: Private licensing
    @author: Alessandro Tanasi
    @contact: alessandro@tanasi.it
    """
    
    
    def __init__(self, results):
        self.res = results
        self.report()
        
        
    
    def report(self):
        """
        Show results
        """

        # Set output vars
        if conf.Paranoid:
            prob = "(confirmed)"
        else:
            prob = "(probable)"

        # Print out report
        log.info("")
        log.info("Results for %s" % self.res.target)
        log.info("Hostname: %s" % self.res.hostname)
        log.info("Served by nameservers (probable): %s" % " ".join(self.res.nameservers))
        log.info("Belongs to domains %s: %s" % (prob, " ".join(self.res.domains)))
        if self.res.vhosts:
            log.info("Aliases enumerated %s:" % prob)
            for h in self.res.vhosts:
                log.info("%s" % h)
        else:
            log.info("No aliases enumerated")
        