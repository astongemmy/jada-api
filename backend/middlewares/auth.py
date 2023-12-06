from flask import request, g, abort
from functools import wraps
import logging

def auth_token_required():
    def decorator(func):
        @wraps(func)
        def middleware(*args, **kwargs):
            auth_key = request.headers.get('X-ROWAPP-AUTH')
            if auth_key:
                try:
                    # key = ndb.Key(urlsafe=auth_key)
                    # token = key.get()
                    token = 'None'
                    if token:
                        access_token = token.user
                        if access_token:
                            setattr(request, 'access_token', access_token)
                            g.access_token = access_token
                            # if token.member:
                            #     member_key = token.member
                            #     entity = member_key.get()
                            #     g.member_key = member_key if entity else None
                            # else:
                            #     g.member_key = None
                        else:
                            logging.error('User key missing in authentication object.')
                            abort(401)

                    else:
                        logging.error('Could not find provided authentication token.')
                        abort(401)

                # except (binascii.Error, DecodeError) as e:
                # logging.warning(str(e))
                except:
                    logging.warning('Invalid access token provided: %s' %auth_key)
                    abort(401)
                
                return func(*args, **kwargs)
            else:
                logging.warning('Authentication header missing in request payload.')
                abort(401)

        return middleware
    
    return decorator