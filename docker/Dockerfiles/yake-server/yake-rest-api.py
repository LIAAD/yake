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

from flask import Flask, jsonify, request

from flasgger import Swagger
import yake

app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'Yake API sample'
}
Swagger(app)

@app.route('/yake/',methods=['POST'])
def handle_yake():
    """Example endpoint return a list of keywords using YAKE
    ---
    parameters:
      - name: text
        in: formData
        type: string
        description: text
        required: true
      - name: language
        in: formData
        type: string
        description: language
        required: true
        default: "en"
        enum: ["pt", "en", "es", "fr", "it", "de" ]
      - name: max_ngram_size
        in: formData
        type: integer
        description: max size of ngram
        required: true
        default: 4
      - name: number_of_keywords
        in: formData
        type: integer
        description: number of keywords to return
        required: true
        default: 10

    responses:
      200:
        description: Extract keywords from input text
    """
    print(request.form)
    text = request.form["text"]
    language = request.form["language"]
    max_ngram_size = int(request.form["max_ngram_size"])
    number_of_keywords = int(request.form["number_of_keywords"])

    my_yake = yake.KeywordExtractor(lan=language,
                                    n=max_ngram_size,
                                    top=number_of_keywords,
                                    dedupLim=0.8,
                                    windowsSize=2
                                    )

    keywords = my_yake.extract_keywords(text)
    result  = [{"ngram":x[1] ,"score":x[0]} for x in keywords]
    return jsonify(result)



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
