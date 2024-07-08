# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.

import logging
import ask_sdk_core.utils as ask_utils
import json
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Load the dataset from the JSON file
try:
    with open('./documents/water_data.json', 'r') as f:
        dataset = json.load(f)
    logger.info("Dataset loaded successfully")
except Exception as e:
    logger.error(f"Error loading dataset: {e}")

# Map user-friendly site names to keys in the dataset
site_map = {
    "amiad filter": "Group_4_pumps_to_Amiad_Filter_Consumption",
    "scale pit": "Group_4_pumps_to_Scale_Pit_Consumption",
    "cold well": "Make_up_line_valve_to_cold_well_Consumption",
    "cooling tower": "VT_Pump_to_cooling_tower_Consumption",
    "ppf pit": "PPF_Pit_to_cold_well_Consumption"
}

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to AquaAssist. How can I help you?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class GetAverageConsumptionIntentHandler(AbstractRequestHandler):
    """Handler for getting average water consumption data."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (
            ask_utils.is_request_type("IntentRequest")(handler_input)
            and ask_utils.is_intent_name("GetAverageConsumptionIntentHandler")(handler_input)
        )

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        try:
            slots = handler_input.request_envelope.request.intent.slots
            site = slots["site"].value.lower()
            logger.info(f"Site requested: {site}")

            # Map the user-friendly site name to the actual dataset key
            site_key = site_map.get(site)
            if not site_key:
                speak_output = f"I couldn't find the site {site}. Please provide a valid site."
                return (
                    handler_input.response_builder
                        .speak(speak_output)
                        .ask(speak_output)
                        .response
                )

            # Calculate the average consumption for the specified site
            total_consumption = 0
            count = 0
            for record in dataset:
                consumption = record.get(site_key)
                if consumption is not None:
                    total_consumption += consumption
                    count += 1

            if count > 0:
                average_consumption = total_consumption / count
                speak_output = f"The average water consumption for {site} is {average_consumption:.2f} units."
            else:
                speak_output = f"No data found for {site}."
        except Exception as e:
            logger.error(f"Error in GetAverageConsumptionIntentHandler: {e}")
            speak_output = "Sorry, I had trouble processing your request. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class GetTotalConsumptionIntentHandler(AbstractRequestHandler):
    """Handler for getting total water consumption data."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (
            ask_utils.is_request_type("IntentRequest")(handler_input)
            and ask_utils.is_intent_name("GetTotalConsumptionIntentHandler")(handler_input)
        )

    def handle(self, handler_input):
        try:
            slots = handler_input.request_envelope.request.intent.slots
            site = slots["site"].value.lower()
            logger.info(f"Site requested: {site}")

            # Map the user-friendly site name to the actual dataset key
            site_key = site_map.get(site)
            if not site_key:
                speak_output = f"I couldn't find the site {site}. Please provide a valid site."
                return (
                    handler_input.response_builder
                        .speak(speak_output)
                        .ask(speak_output)
                        .response
                )

            # Calculate the total consumption for the specified site
            total_consumption = 0
            for record in dataset:
                consumption = record.get(site_key)
                if consumption is not None:
                    total_consumption += consumption

            if total_consumption > 0:
                speak_output = f"The total water consumption for {site} is {total_consumption:.2f} units."
            else:
                speak_output = f"No data found for {site}."
        except Exception as e:
            logger.error(f"Error in GetTotalConsumptionIntentHandler: {e}")
            speak_output = "Sorry, I had trouble processing your request. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "You can ask me for the average or total water consumption for a specific site. How can I help you?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (
            ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input)
            or ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input)
        )

    def handle(self, handler_input):
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # Any cleanup logic goes here.
        return handler_input.response_builder.response

class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(GetAverageConsumptionIntentHandler())
sb.add_request_handler(GetTotalConsumptionIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler())  # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()

