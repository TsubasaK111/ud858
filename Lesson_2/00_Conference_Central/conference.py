#!/usr/bin/env python

"""
conference.py -- Udacity conference server-side Python App Engine API;
    uses Google Cloud Endpoints

$Id: conference.py,v 1.25 2014/05/24 23:42:19 wesc Exp wesc $

created by wesc on 2014 apr 21

"""

__author__ = 'wesc+api@google.com (Wesley Chun)'


from datetime import datetime
import json
import os
import time

import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

from google.appengine.api import urlfetch
from google.appengine.ext import ndb

from models import Profile
from models import ProfileMiniForm
from models import ProfileForm
from models import TeeShirtSize

from settings import WEB_CLIENT_ID


EMAIL_SCOPE = endpoints.EMAIL_SCOPE
API_EXPLORER_CLIENT_ID = endpoints.API_EXPLORER_CLIENT_ID


@endpoints.api( name='conference', version='v1', scopes=[EMAIL_SCOPE]
                allowed_client_ids=[WEB_CLIENT_ID, API_EXPLORER_CLIENT_ID] )
class ConferenceApi(remote.Service):
    """Conference API v0.1"""


    # - - - Helper Functions - - - - - - - - - - - - - - - - - - -

    def _copyProfileToForm(self, profile):
        """Copy relevant fields from Profile to ProfileForm."""
        profileForm = ProfileForm()
        for field in profileForm.all_fields():
            if hasattr(profile, field.name):
                # convert t-shirt string to Enum; just copy others
                if field.name == 'teeShirtSize':
                    setattr( profileForm,
                             field.name,
                             getattr(TeeShirtSize, getattr(profile, field.name)) )
                else:
                    setattr( profileForm,
                             field.name,
                             getattr(profile, field.name) )
        profileForm.check_initialized()
        return profileForm

    def _getProfileFromUser(self):
        """Return user Profile from datastore, creating new one if non-existent."""
        ## TODO 2
        ## step 1: make sure user is authed
        ## uncomment the following lines:
        # user = endpoints.get_current_user()
        # if not user:
        #     raise endpoints.UnauthorizedException('Authorization required')
        profile = None
        ## step 2: create a new Profile from logged in user data
        ## you can use user.nickname() to get displayName
        ## and user.email() to get mainEmail
        if not profile:
            profile = Profile(
                userId = None,
                key = None,
                displayName = "Test",
                mainEmail= None,
                teeShirtSize = str(TeeShirtSize.NOT_SPECIFIED),
            )
        return profile

    def _doProfile(self, save_request=None):
        """Get user Profile and return to user, possibly updating it first."""
        # get user Profile
        profile = self._getProfileFromUser()
        # if saveProfile(), process user-modifiable fields
        if save_request:
            for field in ('displayName', 'teeShirtSize'):
                if hasattr(save_request, field):
                    val = getattr(save_request, field)
                    if val:
                        setattr(profile, field, str(val))
        # return ProfileForm
        return self._copyProfileToForm(profile)


    # - - - Endpoint Routing  - - - - - - - - - - - - - - - - - - -

    @endpoints.method( message_types.VoidMessage, ProfileForm,
                       path='profile', http_method='GET', name='getProfile' )
    def getProfile(self, request):
        """Return user profile."""
        return self._doProfile()
        # TODO 1
        # 1. change request class
        # 2. pass request to _doProfile function

    @endpoints.method( message_types.VoidMessage, ProfileForm,
                       path='profile', http_method='POST', name='saveProfile' )
    def saveProfile(self, request):
        """Update & return user profile."""
        return self._doProfile()


# registers API
api = endpoints.api_server([ConferenceApi])
