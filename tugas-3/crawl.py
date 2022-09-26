from calendar import c
import imp
from os import link
import requests
from bs4 import BeautifulSoup
import csv

def isDefined(label):
    if label:
        return label
    else:
        return '-'

link_kategori = [
    'hearing-aids','lainnya'
]

# yg belum berhasil di scrape
# alergi, demam, makanan, hiper, 

for nama_kategori in link_kategori:
    url = "https://www.halodoc.com/obat-dan-vitamin/kategori/"+nama_kategori

    # Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27"

    }


    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")

    clas = "custom-container__list__container__item d-flex flex-column justify-content-start align-items-center ng-star-inserted"
    items = soup.findAll("li", clas)
    clas_a = "custom-container__list__container__item--link ng-star-inserted"

    array_data = []


    for it in items:

        

        link = it.find("a",clas_a)
        # print(link.get("href"))

        detail_url = "https://www.halodoc.com" + link.get("href") 
        req_detail = requests.get(detail_url, headers=headers)
        soup_detail = BeautifulSoup(req_detail.text, "html.parser")


        product_name = soup_detail.find('h1', 'product-label').text
        # print("------"+product_name.text+"------")



        product_detail = soup_detail.findAll("div", "property-container col-lg-12 col-md-12 ng-star-inserted")
        prod_detail_category = soup_detail.find("div", "drug-detail col-md-12 margin-b-20 pb-3 ng-star-inserted")
        category = prod_detail_category.find("a").find("span").text
        # print("kategori:" + category)



        desc = ind = dos = atur = '-'
        for prod in product_detail:

            checkDesc = prod.find("div", "drug-list col-md-12").find('div','ttl-list').text
            if checkDesc.lower() == 'deskripsi':
                desc = prod.find('div', 'drug-detail col-md-12 margin-b-20 ng-star-inserted').find('div').text
            elif checkDesc.lower() == 'indikasi umum':
                ind = prod.find('div', 'drug-detail col-md-12 margin-b-20 ng-star-inserted').find('div').text
            elif checkDesc.lower() == 'dosis':
                dos = prod.find('div', 'drug-detail col-md-12 margin-b-20 ng-star-inserted').find('div').text
            elif checkDesc.lower() == 'aturan pakai':
                atur = prod.find('div', 'drug-detail col-md-12 margin-b-20 ng-star-inserted').find('div').text
             

        dict_data = {
            'product_name':isDefined(product_name),
            'category':isDefined( category),
            'deskripsi':desc,
            'indikasi_umum':ind,
            'dosis':dos,
            'aturan_pakai':atur,
        }

        array_data.append(dict_data)


    try:
        # with open("data_batukflu.csv", 'w',newline='') as csvfile:
        #     writer = csv.DictWriter(csvfile, fieldnames=column)
        #     writer.writeheader()
        #     for key in array_data:
        #         writer.writerow(key)
        filename = nama_kategori+'.csv'
        keys = array_data[0].keys()
        a_file = open(filename, "w")
        dict_writer = csv.DictWriter(a_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(array_data)
        a_file.close()
    except IOError:
        print("I/O error")





