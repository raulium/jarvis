#!/usr/local/env python

# ============== CONFIG PARAMETERS
# ============== INTERNAL LIBRARIES
from web_mod import ripText


# ============== EXTERNAL LIBRARIES

def labStatus():
    """Check status of the Laboratory, returning 0 if open & 1 if closed"""
    statMSG = ripText("http://www.ll.mit.edu/status/index.html")
    if "closed" in str(statMSG[0]):
        return 1
    if "open" in str(statMSG[0]):
        return 0
