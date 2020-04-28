# Uses flask server to do inferences
import flask
import pandas as pd
from summarizer import Summarizer


# A singleton for holding the model. This simply loads the model and holds it.
# It has a predict function that does a prediction based on the model and the input data.

class PredictService(object):
    model = None  # Where we keep the model when it's loaded

    @classmethod
    def get_model(cls):
        """Get the model object for this instance, loading it if it's not already loaded."""
        if cls.model is None:
            print("getting model in PredictService")
            cls.model = Summarizer()
        return cls.model

    @classmethod
    def predict(cls, data):
        """For the input, do the predictions and return them.

        Args:
            data (a pandas dataframe): The data on which to do the predictions. There will be
                one prediction per row in the dataframe"""
        my_model = cls.get_model()
        print("start ti call model")
        summary = my_model(data)
        return summary


# The flask app for serving predictions
app = flask.Flask(__name__)


@app.route('/ping', methods=['GET'])
def ping():
    """Determine if the container is working and healthy. In this sample container, we declare
    it healthy if we can load the model successfully."""
    health = PredictService.get_model() is not None  # You can insert a health check here

    status = 200 if health else 404
    return flask.Response(response='\n', status=status, mimetype='application/json')


@app.route('/invocations', methods=['POST'])
def transformation():
    """Do an inference on a single batch of data. In this sample server, we take data as Json or CSV, convert
    it to a pandas data frame and convert the predictions back to CSV (which really
    just means one prediction per line, since there's a single column.
    """
    data = None  # default a test data

    print("start predicating:")

    if flask.request.content_type == 'application/json' or flask.request.content_type == 'text/csv':
        decoded = flask.request.data.decode('utf-8')
        print("decoded is: ", decoded)
        data = decoded.replace('\r', '').split('\n')
        print("data is: ", data)

    # Do the prediction
    summary = PredictService.predict(decoded)
    print("returning: ", summary)
    # Convert from numpy back to JSON
    result = pd.DataFrame({'summary': summary}, index=[0]).to_json(orient='records')

    return flask.Response(response=result, status=200)
