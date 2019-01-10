#!/usr/bin/env python
"""
Copyright (c) 2019. All rights reserved.
@author:        salman malik
@created:       1/4/19
@last modified: 1/8/19
"""
from __future__ import print_function
from botocore.vendored import requests
from datetime import datetime
import json

# --------------- Helpers that build all of the responses ----------------------

#NOTE: can't use the word 'speechlet' in text output for cards
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_ssml_speechlet_response(title, speech_output, text_output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': speech_output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': text_output
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
def get_location(context):
    apiEndpoint = context['System']['apiEndpoint']
    deviceId = context['System']['device']['deviceId']
    apiAccessToken = context['System']['apiAccessToken']
    url =  '{}/v1/devices/{}/settings/address/countryAndPostalCode'.format(apiEndpoint, deviceId)
    headers = {'Accept': 'application/json', 'Authorization': 'Bearer {}'.format(apiAccessToken)}
    r = requests.get(url, headers=headers)
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
    speech_output = "<speak> <s>Assalamu Alaykum <break strength='medium'/> welcome to the Prayer Times skill.</s> <s> You can ask me what time a specific prayer is.</s> <s> For example <break strength='medium'/> you can say <break strength='medium'/> When is Fajr? </s> </speak>"
    text_output = "Assalamu Alaykum, welcome to the Prayer Times skill. You can ask me what time a specific prayer is. For example, you can say: 'When is Fajr?'"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Assalamu Alaykum, welcome to the Prayer Times skill. You can ask me what time a specific prayer is. For example, you can say: 'When is Fajr?'"
    should_end_session = False

    return build_response(session_attributes, build_ssml_speechlet_response(
        card_title, speech_output, text_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "May Allah Bless You."
    # Setting this to true ends the session and exits the skill.
    should_end_session = True

    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# This url uses zipcode:
# 'http://api.aladhan.com/v1/timingsByAddress?address=20009'

# Method for getting specific prayer times
def when_is_prayer(prayer, zipcode):
    r = requests.get('http://api.aladhan.com/v1/timingsByAddress?address=' + zipcode + '&method=2')
    r = r.json()
    r = r['data']['timings'][prayer]
    d = datetime.strptime(r, "%H:%M")
    d = d.strftime("%I:%M %p")
    return d

def set_prayer_in_session(intent_request, session, context):
    prayer = intent_request['slots']['prayer']['value']
    zipcode = get_location(context)

    if prayer == 'fajr':
       card_title = prayer + " is at " + when_is_prayer('Fajr', zipcode)
       speech_output = prayer + " is at " + when_is_prayer('Fajr', zipcode)
       should_end_session = True
    elif prayer == 'dhuhr':
       card_title = prayer + " is at " + when_is_prayer('Dhuhr', zipcode)
       speech_output = prayer + " is at " + when_is_prayer('Dhuhr', zipcode)
       should_end_session = True
    elif prayer == 'asr':
           card_title = prayer + " is at " + when_is_prayer('Asr', zipcode)
           speech_output = prayer + " is at " + when_is_prayer('Asr', zipcode)
           should_end_session = True
    elif prayer == 'maghrib':
           card_title = prayer + " is at " + when_is_prayer('Maghrib', zipcode)
           speech_output = prayer + " is at " + when_is_prayer('Maghrib', zipcode)
           should_end_session = True
    elif prayer == 'Isha':
           card_title = prayer + " is at " + when_is_prayer('Isha', zipcode)
           speech_output = prayer + " is at " + when_is_prayer('Isha', zipcode)
           should_end_session = True
    else:
      card_title = "Invalid Prayer"
      speech_output = "Invalid Prayer, please try again"
      should_end_session = False

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

def on_intent(intent_request, session, context):
    """ Called when the user specifies an intent for this skill """
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    session = session
    context = context
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "PrayerTimeIntent":
        return set_prayer_in_session(intent, session, context)
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
        return on_intent(event['request'], event['session'], event['context'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])