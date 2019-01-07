#!/usr/bin/env python
"""
Copyright (c) 2019. All rights reserved.
@author salman malik
@since 1/4/19
"""
from __future__ import print_function
from botocore.vendored import requests
from datetime import datetime
import json

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# Helper method to determine zipcode of the user
def get_location(request, context):
    deviceId = context['device']['deviceId']
    token = context['user']['permissions']['consentToken']
    url = 'https://api.amazonalexa.com/v1/devices/{}/settings/address/countryAndPostalCode'.format(deviceId)
    headers = {'Accept': 'application/json', 'Authorization': 'Bearer {}'.format(token)}
    r = requests.get(url, headers=header)
    if r.status_code == 200:
        r = r.json()
        return r['postalCode']

# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Prayer Times app. " \
                    "You can ask me what time a specific prayer is." \
                    "For example you can say when is Fajr?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "You can ask me what time a specific prayer." \
                    "For example, you can says when is Fajr?"
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "May Allah Bless You."
    # Setting this to true ends the session and exits the skill.
    should_end_session = True

    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# This url uses zipcode:
# 'http://api.aladhan.com/v1/timingsByAddress?address=20009'

# Methods for getting specific prayter times
def when_is_fajr():
    r = requests.get('http://api.aladhan.com/v1/timingsByCity?city=DC&country=US&method=2')
    r = r.json()
    r = r['data']['timings']['Fajr']
    d = datetime.strptime(r, "%H:%M")
    d = d.strftime("%I:%M %p")
    return d

def when_is_dhuhr():
    r = requests.get('http://api.aladhan.com/v1/timingsByCity?city=DC&country=US&method=2')
    r = r.json()
    r = r['data']['timings']['Dhuhr']
    d = datetime.strptime(r, "%H:%M")
    d = d.strftime("%I:%M %p")
    return d

def when_is_asr():
    r = requests.get('http://api.aladhan.com/v1/timingsByCity?city=DC&country=US&method=2')
    r = r.json()
    r = r['data']['timings']['Asr']
    d = datetime.strptime(r, "%H:%M")
    d = d.strftime("%I:%M %p")
    return d

def when_is_maghrib():
    r = requests.get('http://api.aladhan.com/v1/timingsByCity?city=DC&country=US&method=2')
    r = r.json()
    r = r['data']['timings']['Maghrib']
    d = datetime.strptime(r, "%H:%M")
    d = d.strftime("%I:%M %p")
    return d

def when_is_isha():
    r = requests.get('http://api.aladhan.com/v1/timingsByCity?city=DC&country=US&method=2')
    r = r.json()
    r = r['data']['timings']['Isha']
    d = datetime.strptime(r, "%H:%M")
    d = d.strftime("%I:%M %p")
    return d

def set_prayer_in_session(intent_request, session):
    prayer = intent_request['slots']['prayer']['value']

    if prayer == 'fajr':
       card_title = prayer + " is at " + when_is_fajr()
       speech_output = prayer + " is at " + when_is_fajr()
       should_end_session = True
    elif prayer == 'dhuhr':
       card_title = prayer + " is at " + when_is_dhuhr()
       speech_output = prayer + " is at " + when_is_dhuhr()
       should_end_session = True
    elif prayer == 'asr':
           card_title = prayer + " is at " + when_is_asr()
           speech_output = prayer + " is at " + when_is_asr()
           should_end_session = True
    elif prayer == 'maghrib':
           card_title = prayer + " is at " + when_is_maghrib()
           speech_output = prayer + " is at " + when_is_maghrib()
           should_end_session = True
    elif prayer == 'Isha':
           card_title = prayer + " is at " + when_is_isha()
           speech_output = prayer + " is at " + when_is_isha()
           should_end_session = True
    else:
      card_title = "Invalid Prayer"
      speech_output = "Invalid Prayer, please try again"

    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    session = session
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "PrayerTimeIntent":
        return set_prayer_in_session(intent, session)
        # return set_prayer_in_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])


    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])