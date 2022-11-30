# url = "https://xakep.ru/2022/11/25/eighth-chrome-0day/"
# url_id = url.split("/")[-5:-1]
# article_id = "_".join(url_id)
# print(article_id)


i = 100

for k in range(2, i):
    c = 0
    for l in range(2, k):
        if k % l == 0:
            c += 1
    if c <= 1:
       print(f'Число {k} натуральное')