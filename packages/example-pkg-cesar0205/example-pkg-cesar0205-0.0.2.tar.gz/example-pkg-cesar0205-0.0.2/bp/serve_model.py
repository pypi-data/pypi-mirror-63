import sys
import logging
import os

_logger = logging.getLogger(__name__)

RANDOM_STATE = 0
SPLIT_PCT = 0.1

def serve_model() -> None:
    if len(sys.argv) > 0:
        model_id = sys.argv[1]
        os.system(f'mlflow models serve -m mlruns/0/{model_id}/artifacts/model -p 1234')


if __name__ == '__main__':
    serve_model()
