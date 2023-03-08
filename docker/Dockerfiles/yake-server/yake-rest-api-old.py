"""
Credits @arianpasquali
https://gist.githubusercontent.com/arianpasquali/16b2b0ab2095ee35dbede4dd2f4f8520/raw/ba4ea7da0d958fc4b1b2e694f45f17cc71d8238d/yake_rest_api.py

The simple example serving YAKE as a rest api.

instructions:

 pip install flasgger
 pip install git+https://github.com/LIAAD/yake

 python yake_rest_api.py

open http://127.0.0.1:5000/apidocs/
"""

from flasgger import Swagger
from flask import Flask, jsonify, request

try:
    import simplejson as json
except ImportError:
    import json
try:
    from http import HTTPStatus
except ImportError:
    import httplib as HTTPStatus

import yake

app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'Yake API Explorer',
    'uiversion': 3
}
swagger = Swagger(app)


@swagger.validate('content')
@app.route('/yake/', methods=['POST'])
def handle_yake():
    """Example endpoint return a list of keywords using YAKE
    ---
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
        - name: content
          in: body
          description: content object
          required: true
          schema:
            $ref: '#/definitions/content'

    requestBody:
        description: Optional description in *Markdown*
        required: true
        content:
          application/json:
            schema:
              id: content
              type: object


    responses:
      200:
        description: Extract keywords from input text
        schema:
            $ref: '#/definitions/result'

    definitions:
      content:
        description: content object
        properties:
          text:
            type: string
          language:
            type: string
          max_ngram_size:
            type: integer
            minimum: 1
          number_of_keywords:
            type: integer
            minimum: 1
        required:
          - text
          - language
          - max_ngram_size
          - number_of_keywords
        example:   # Sample object
            text: Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning   competitions. Details about the transaction remain somewhat vague , but given that Google is hosting   its Cloud Next conference in San Francisco this week, the official announcement could come as early   as tomorrow.  Reached by phone, Kaggle co-founder CEO Anthony Goldbloom declined to deny that the   acquisition is happening. Google itself declined 'to comment on rumors'.   Kaggle, which has about half a million data scientists on its platform, was founded by Goldbloom   and Ben Hamner in 2010. The service got an early start and even though it has a few competitors   like DrivenData, TopCoder and HackerRank, it has managed to stay well ahead of them by focusing on its   specific niche. The service is basically the de facto home for running data science  and machine learning   competitions.  With Kaggle, Google is buying one of the largest and most active communities for   data scientists - and with that, it will get increased mindshare in this community, too   (though it already has plenty of that thanks to Tensorflow and other projects).   Kaggle has a bit of a history with Google, too, but that's pretty recent. Earlier this month,   Google and Kaggle teamed up to host a $100,000 machine learning competition around classifying   YouTube videos. That competition had some deep integrations with the Google Cloud Platform, too.   Our understanding is that Google will keep the service running - likely under its current name.   While the acquisition is probably more about Kaggle's community than technology, Kaggle did build   some interesting tools for hosting its competition and 'kernels', too. On Kaggle, kernels are   basically the source code for analyzing data sets and developers can share this code on the   platform (the company previously called them 'scripts').  Like similar competition centric sites,   Kaggle also runs a job board, too. It's unclear what Google will do with that part of the service.   According to Crunchbase, Kaggle raised $12.5 million (though PitchBook says it's $12.75) since its   launch in 2010. Investors in Kaggle include Index Ventures, SV Angel, Max Levchin, Naval Ravikant,   Google chief economist Hal Varian, Khosla Ventures and Yuri Milner
            language: en
            max_ngram_size: 3
            number_of_keywords: 10
      result:
        type: array
        items:
          minItems: 0
          type: object
          required:
            - name
            - value
          properties:
            ngram:
              type: string
            score:
              type: number
    """

    try:
        assert request.json["text"], "Invalid text"
        assert len(request.json["language"]) == 2, "Invalid language code"
        assert int(request.json["max_ngram_size"]), "Invalid max_ngram_size, Suggested max_ngram_size setting of 1 or 2 or 3"
        assert int(request.json["number_of_keywords"]), "Invalid number_of_keywords"
        assert int(request.json["windows_size"]), "Invalid windows_size, Suggested windows_size setting of 1 or 2"

        text = request.json["text"]
        language = request.json["language"]
        max_ngram_size = int(request.json["max_ngram_size"])
        number_of_keywords = int(request.json["number_of_keywords"])
        windows_size = int(request.json["windows_size"])

        my_yake = yake.KeywordExtractor(lan=language,
                                        n=max_ngram_size,
                                        top=number_of_keywords,
                                        dedupLim=-1,
                                        windowsSize=windows_size
                                        )

        keywords = my_yake.extract_keywords(text)
        result = [{"keyword": x[0], "score": x[1]} for x in keywords]

        return jsonify(result), HTTPStatus.OK
    except IOError as e:
        return jsonify("Language not supported"), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify(str(e)), HTTPStatus.BAD_REQUEST





if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
