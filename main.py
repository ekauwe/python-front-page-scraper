#!/usr/bin/env python

import requests
import re
import sys
import codecs
import argparse
import textwrap

#############################
# cmd line arguments
#############################

parser = parser = argparse.ArgumentParser(
     prog='PROG',
     formatter_class=argparse.RawDescriptionHelpFormatter,
     description=textwrap.dedent('''\
         URL scraper.
         --------------------------------
         Scrape page:
         %s -s https://www.google.com
         %s --site https://www.google.com

         Scrape and save:
         %s -s https://www.google.com -o test.hmtl
         %s --site https://www.google.com -o test.html

         ''' % (sys.argv[0], sys.argv[0], sys.argv[0], sys.argv[0])))

parser.add_argument('--site','-s', dest='site', action='store',
                    default=False, help='-s, --site https://www.google.com')
parser.add_argument('--ouput','-o', dest='output', action='store',
                    default=False, help='-o, --output <file.hmtl>')

args = parser.parse_args()

#############################
#  requirements
#############################
if not args.site:
    parser.error('please see help menu')

if args.output and not args.site:
    parser.error('please see help menu')

#############################
#  URL scraper
#############################

def scrape(link):
    res=requests.get(link)
    if res.status_code == 200:
        res=re.sub('head>', 'head>\n<base href='+link+' target=\"_blank\"\>', res.text)

        if args.output:
            f=codecs.open(args.output, 'w', 'utf-8') 
            f.write(res)
            f.close()

        else:
            print res

    else:
        exit('page not reachable')

#############################
#  check site/url
#############################
def check():
    if args.site[:4] != 'http':
        return 'http://'+ args.site
    else: 
        return args.site

#############################
#  main
#############################
def main():
    print args.site, args.output
    url = check()
    print url
    scrape(url)

#############################
#  launch
#############################
main()