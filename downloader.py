#!/usr/bin/env python
import logging
import sys
import argparse
import urllib
import os
import shutil
# Make sure the flickrapi module from the source distribution is used
sys.path.insert(0, 'flickrapi')
import flickrapi

logging.basicConfig(
        format = '%(asctime)s %(name)s %(levelname)s: %(message)s',
#        filename = logfile,
#        level = logging.DEBUG)
        level = logging.INFO)
mainlogger = logging.getLogger(__name__)
mainlogger.info('running flickr downloading client')

class FlickrAccess:
    def __init__(self):
        #api_key =    unicode(os.environ['API_KEY'])
        #api_secret = unicode(os.environ['API_SECRET'])
        api_key =     os.environ['API_KEY']
        api_secret =  os.environ['API_SECRET']
        self.logger = logging.getLogger(__name__ + '.FlickrAccess')
        self.flickr = flickrapi.FlickrAPI(api_key, api_secret, store_token = True)
    
    def ensurePermission(self, perm):
        uperm = perm #unicode(perm)
        if not self.flickr.token_valid(perms=uperm):
            self.logger.info('acquire permission ' + uperm)
            # Get a request token
            self.flickr.get_request_token(oauth_callback='oob')
            
            # Open a browser at the authentication URL. Do this however
            # you want, as long as the user visits that URL.
            authorize_url = self.flickr.auth_url(perms=uperm)
            #webbrowser.open_new_tab(authorize_url)
            print(' Please paste this URL into your browser and copy the verification code: ' + authorize_url)
            
            # Get the verifier code from the user. Do this however you
            # want, as long as the user gives the application the code.
            verifier = input(' Verifier code: ')

            # Trade the request token for an access token
            self.flickr.get_access_token(verifier)

class DownloadIt:
    def __init__(self, flickraccess):
        assert flickraccess != None
        flickraccess.ensurePermission('read')
        self.flickr = flickraccess.flickr

    def run(self):
        walkingcount = 0
        for walkingphoto in self.flickr.walk(user_id = 'me', extras = 'url_o', per_page = '500'):
            walkingcount += 1
            photoid = walkingphoto.get('id')
            urlo = walkingphoto.get('url_o')
            print('checking #' + str(walkingcount) + ': ' + photoid + ', url_o: ' + urlo)
            dest_filename = photoid + '.jpg'
            if os.path.exists(dest_filename):
                print('  skip')
            else:
                local_filename, headers = urllib.request.urlretrieve(urlo)
                shutil.move(local_filename, dest_filename)

def main(argv):
    parser = argparse.ArgumentParser(description='Upload photos to flickr and avoid duplicates.')
    parser.add_argument('--downloadall', action='store_true', help='Download all images in O')
    parser.add_argument('--debug', action='store_true', help='Debug logging')
    args = parser.parse_args()
    #print(args)

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        mainlogger.debug(str(args))
    if args.downloadall:
        DownloadIt(FlickrAccess()).run()
    else:
        parser.print_help()

if __name__ == "__main__":
    main(sys.argv)
