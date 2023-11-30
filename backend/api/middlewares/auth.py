from flask_restx import abort
from flask import request, g
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
                            logging.error('User key missing in authentication object')
                            abort(403, message='Access denied', status=False, error=403)
                    else:
                        logging.error('No authentication key provided')
                        abort(403, message='Access denied', status=False, error=403)
                # except (binascii.Error, DecodeError) as e:
                except:
                    # logging.warning(str(e))
                    logging.warning("Invalid access token provided: %s" %auth_key)
                    abort(403, message='Access denied', status=False, error=403)
                
                return func(*args, **kwargs)
            else:
                abort(403, message='Access denied', status=False, error=403)
        return middleware
    return decorator