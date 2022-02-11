from flask import Flask, render_template, request, jsonify
import urllib.request
import json

app = Flask(__name__)

@app.route('/') # localhost:5000
def hello_world():
    # return '<p>Hello, World!</p>'
    return render_template('index.html')


client_id = 'BRxQGq5dEtqSNALD60JO'
client_secret = 'yq2SZXjGq7'

@app.route('/translate', methods = ['POST'])
def do_papago():
    translated_text = ''
    if request.method == "POST":
        # print(type(request.json), request.json) # dict, 

        # 감지 & 번역 공동 API Key
        text, target_language = request.json.values()

        # 언어 감지 함수 호출
        source_language = neural_machine_translation(text)

        encoded_text = urllib.parse.quote(text)
        data = f'source={source_language}&target={target_language}&text=' + encoded_text

        # 번역 API 요청(HTTP Request)
        url = "https://openapi.naver.com/v1/papago/n2mt"
        api_request = urllib.request.Request(url)

        # HTTP 요청 헤더(Request header)에 클라이언트 아이디와 클라이언트 시크릿 추가.
        api_request.add_header("X-Naver-Client-Id",client_id)
        api_request.add_header("X-Naver-Client-Secret",client_secret)

        # 번역 API 응답(HTTP Response) - HTTP 요청에 따른 응답.
        response = urllib.request.urlopen(api_request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read() # bytes

            response_body = response_body.decode('utf-8') # str
            print(type(response_body), response_body) # <class 'str'> {'message': {'@type': 'response'
            # print(type(jsonify(response_body))) # flask.wrappers.response

            response_json = json.loads(response_body)
            print(type(response_json), response_json) # <class 'dict'> {'message': {'@type': 'response'
            translated_text = response_json['message']['result']['translatedText']
            
            # print(chardet.detect(translated_text.encode())) # {'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}
            data = {
                'translated_text': translated_text
            }                  

        else:
            print("Error Code:" + rescode)

        return jsonify(data)

# 
def neural_machine_translation(text):
    encoded_query = urllib.parse.quote(text)
    data = 'query=' + encoded_query

    # 언어 감지 API 요청(HTTP Request)
    ntm_url = "https://openapi.naver.com/v1/papago/detectLangs"
    request = urllib.request.Request(ntm_url)

    # HTTP 요청 헤더(Request header)에 클라이언트 아이디와 클라이언트 시크릿 추가.
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)

    # 언어 감지 API 응답(HTTP Response) - HTTP 요청에 따른 응답.
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    source_lang_code = '' # 감지된 언어 코드를 담을 변수

    if(rescode==200):
        response_body = response.read()
        print(type(response_body.decode('utf-8')), response_body.decode('utf-8')) # <class 'str'> {"langCode":"ko"}
        parsed_to_json = json.loads(response_body.decode('utf-8')) # convert str to dict(JSON form)
        print(type(parsed_to_json), parsed_to_json) # <class 'dict'> {'langCode': 'ko'}    
        source_lang_code = parsed_to_json['langCode']

    else:
        print("Error Code:" + rescode)

    print(f'감지된 언어 코드 : {source_lang_code}') # ex) ko
    return source_lang_code

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)