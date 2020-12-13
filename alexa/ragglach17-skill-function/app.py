import json

# import requests
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name, is_request_type
from ask_sdk_core.skill_builder import SkillBuilder

from ask_sdk_model.response import Response
from ask_sdk_model import ui

import pool


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        print("LaunchRequest")
        response_builder = handler_input.response_builder
        speech = 'Hallo. Wie kann ich dir helfen?'
        response_builder\
            .set_card(ui.SimpleCard("Hallo!", "Wie kann ich dir helfen?"))\
            .set_should_end_session(False)\
            .speak(speech)\
            .ask("Sag zum Beispiel: Welche Temperatur hat der Pool?")
        return response_builder.response

class SwimmingPoolTemperatureIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("SwimmingPoolTemperatureIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        print("SwimmingPoolTemperatureIntent")
        response_builder = pool.get_pool_temperature_response_data(handler_input)
        return response_builder.response

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        print("HelpIntent")
        speech = "Hallo! Ich helfe dir dabei dein Haus zu steuern. Sag zum Beispiel: Welche Temperatur hat der Pool?"
        handler_input.response_builder.speak(speech)\
            .set_card(ui.SimpleCard("Ragglach 17", speech)) \
            .speak(speech)\
            .set_should_end_session(False)\
            .ask("Wie kann ich dir helfen?")
        return handler_input.response_builder.response

class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        print("FallbackIntent")
        speech = "Tut mir Leid. Das habe ich leider nicht verstanden. Kannst du das wiederholen?"
        handler_input.response_builder.speak(speech)\
            .set_should_end_session(False)\
            .ask("Kannst du deine Frage wiederholen?") \
            .speak(speech)
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        print("CancelOrStopIntent")
        speech = "Servus"
        handler_input.response_builder\
            .set_should_end_session(True)\
            .speak(speech)
        return handler_input.response_builder.response

class CatchAllExceptionHandler(AbstractExceptionHandler):

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response

        print("CatchAllExceptionHandler")
        handler_input.response_builder\
            .speak("Es tut mir Leid. Leider ist etwas schiefgelaufen "
                   "und ich kann deine Frage im Moment nicht beantworten.")\
            .set_should_end_session(True)\

        return handler_input.response_builder.response


sb = SkillBuilder()
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(SwimmingPoolTemperatureIntentHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()
