#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

if __name__ == '__main__':

    import sys, os
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'annonex2embl'))
    try:
        from annonex2embl import CLIOps
    except:
        import CLIOps

    CLIOps.start_annonex2embl()
