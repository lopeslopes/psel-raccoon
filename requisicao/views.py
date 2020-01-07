from django.http import HttpResponse
import requests
import json

# Create your views here.

def segundo_termo(termo):
    return termo[1]

def home(request):
    posts = []
    url = 'https://us-central1-psel-clt-ti-junho-2019.cloudfunctions.net/psel_2019_get'
    response = requests.get(url)
    res = json.loads(response.text)


    ''' item a '''
    promocao = []

    for post in res['posts']:
        if 'promocao' in post['title']:
            aux1 = [post['product_id'], post['price']]
            if aux1 not in promocao:
                promocao.append(aux1)
            
    promocao.sort(key=segundo_termo)
    ''' fim item a '''


    ''' item b '''
    likes = []

    for post in res['posts']:
        if 'instagram_cpc' in post['media']: 
            if int(post['likes']) > 700:
                aux1 = [post['post_id'], post['price']]
                if aux1 not in likes:
                    likes.append(aux1)
            
    likes.sort(key=segundo_termo)
    ''' fim item b '''


    ''' item c '''
    total_likes = 0

    for post in res['posts']:
        if ('instagram_cpc' in post['media']) or ('google_cpc' in post['media']) or ('facebook_cpc' in post['media']): 
            if ((post['date'][3:5]) == '05') and (post['date'][6:10]) == '2019':
                total_likes = total_likes + int(post['likes'])      
    ''' fim item c '''


    ''' item d '''
    url2 = 'https://us-central1-psel-clt-ti-junho-2019.cloudfunctions.net/psel_2019_get_error'
    response2 = requests.get(url2)
    res2 = json.loads(response2.text)

    erro = []
    todos_produtos = []

    for post in res2['posts']:
        aux1 = [post['product_id'], post['price']]
        if aux1 not in todos_produtos:
            flag = 0
            for produto in todos_produtos:
                if aux1[0] == produto[0]:
                    flag = 1
            if flag == 0:
                todos_produtos.append(aux1)
            elif flag == 1:
                erro.append(aux1[0])

    erro.sort()
    ''' fim item d '''


    ''' montagem do arquivo resposta '''
    res_a = [{"product_id": item[0], "price_field": item[1]} for item in promocao]
    res_b = [{"post_id": item[0], "price_field": item[1]} for item in likes]
    res_d = [item for item in erro]

    resposta_py = {
        'full_name': "Mateus Lopes Mazziero",
        'email': "mateuslmazziero@gmail.com",
        'code_link': "www.github.com/lopeslopes/psel-raccoon",
        'response_a': res_a,
        'response_b': res_b,
        'response_c': total_likes,
        'response_d': res_d
    }

    with open('resposta.json', 'w') as arq:
        json.dump(resposta_py, arq)
    ''' fim do arquivo resposta '''


    ''' post request da resposta '''
    '''
    url = 'https://us-central1-psel-clt-ti-junho-2019.cloudfunctions.net/psel_2019_post'
    aux = json.dumps(resposta_py)
    r = requests.post(url, json=aux)
    '''
    '''final do post request'''

    html = '<p>Processo finalizado</p>'

    return HttpResponse(html)