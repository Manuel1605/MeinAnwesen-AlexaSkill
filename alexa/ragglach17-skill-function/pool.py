import time
from ask_sdk_model import ui
import dynamodb


def get_pool_temperature_response_data(handler_input):
    pool_temperature = round(dynamodb.query_pool_temperature(time))
    response_builder = handler_input.response_builder

    if pool_temperature is not None:

        speech = f'Die Pool Temperatur beträgt {pool_temperature} Grad'
        card = ui.SimpleCard("Pool Temperatur", f'{pool_temperature}° C')
    else:
        speech = 'Es sind leider keine Sensordaten verfügbar'
        card = None

    return response_builder \
        .set_card(card) \
        .set_should_end_session(True) \
        .speak(speech)
