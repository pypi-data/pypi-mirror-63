import yandex_search 

yandex = yandex_search.Yandex(api_user='ggurga11', api_key='03.193801943:ce2619819590278cf386104bb0258b21')

def yandex_query(key_word):
    text = key_word
    results = yandex.search(text)
    list_results = results.items
    list_len = len(list_results)
    for i in range(list_len-1):
        c = list_results[i]
        print(c['title'],' - ',c['url'],'\n' )


