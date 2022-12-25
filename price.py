import streamlit as st
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

st.title('Product Search')

def scrape_flipkart(item):
    url = 'https://flipkart.com/search?q='+str(item)
    r = requests.get(url)
    htmlcontent = r.content
    soup = BeautifulSoup(htmlcontent, 'html.parser')
    try:
        link = soup.find("a", {"class": "_2rpwqI"}).attrs['href']
    except:
        pass
    try:
        link = soup.find("a", {"class": "_1fQZEK"}).attrs['href']
    except:
        pass
    try:
        link = soup.find("a", {"class": "_2UzuFa"}).attrs['href']
    except:
        pass
    link = "https://flipkart.com"+str(link)
    r = requests.get(link)
    htmlcontent = r.content
    soup = BeautifulSoup(htmlcontent, 'html.parser')
    st.write("\nFLIPKART:")
    name = soup.find('span', "B_NuCI")
    st.write("name: ", name.text)
    price = soup.find('div', {'class': '_30jeq3 _16Jk6d'})
    st.write("price: ", price.text)
    rating = soup.find('div', {'class': '_3LWZlK'})
    st.write("ratings:", rating.text)
    st.write("link: ", link)

def scrape_amazon(item):
    ua = UserAgent()
    hdr = {'User-Agent': ua.random,
           'Accept-Language': 'en-US,en;q=0.8'}
    url = 'https://www.amazon.in/s?k='+str(item)
    r = requests.get(url, headers=hdr)
    htmlcontent = r.content
    soup = BeautifulSoup(htmlcontent, 'html.parser')
    product = soup.find_all(
        "a", {"class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})[0]
    link = "https://www.amazon.in"+str(product['href'])
    r = requests.get(link, headers=hdr)
    htmlcontent = r.content
    soup = BeautifulSoup(htmlcontent, 'html.parser')
    st.write("\nAMAZON:")
    name = soup.find('span', "a-size-large product-title-word-break")
    st.write("name:", name.text)
    price = soup.find('span', {'class': 'a-offscreen'})
    st.write("price: ", price.text)
    rating = soup.find('span', "a-icon-alt")
    st.write("ratings:", rating.text)
    st.write("link: ", link)

def scrape_reliance(item):
    url = 'https://www.reliancedigital.in/search?q='+str(item)
    r = requests.get(url)
    htmlcontent = r.content
    soup = BeautifulSoup(htmlcontent, 'html.parser')
    product = soup.find_all('div', class_='sp grid')[0]
    for i in product:
        link = i.get('href')
    link = "https://www.reliancedigital.in"+str(link)
    r = requests.get(link)
    htmlcontent = r.content
    soup = BeautifulSoup(htmlcontent, 'html.parser')
    st.write("\nRELIANCE DIGITAL:")
    name = soup.find('h1', "pdp__title mb__20")
    st.write("name:", name.text)
    price = soup.find('span', {'class': 'pdp__offerPrice'})
    st.write("price:", price.text)
    st.write("link: ", link)


def main():
    st.sidebar.title('Product Search')
    item = st.sidebar.text_input('Enter product:')
    websites = st.sidebar.multiselect(
        'Select websites:', ['Flipkart', 'Amazon', 'Reliance Digital'])
    if 'Flipkart' in websites:
        scrape_flipkart(item)
    if 'Amazon' in websites:
        scrape_amazon(item)
    if 'Reliance Digital' in websites:
        scrape_reliance(item)

if __name__ == '__main__':
    main()
