# importing libraries
from bs4 import BeautifulSoup
import requests
import csv
import regex

  
def main(URL, links_counter):
    # openning our output file in append mode
    File = open("out.csv", "a", encoding='utf-8')
    if links_counter ==0:
        File.write("Title,")
        File.write("Price,")
        File.write("Rating,")
        File.write("Review,")
        File.write("Availability,")
        File.write("Material,")
        File.write("Color,")
        File.write("Style,")
        File.write("Brand,")
        File.write("Item Dimension L*W*H,")
        File.write("Pattern,")
        File.write("Item Weight,")
        File.write("Age Range,")
        File.write("Capacity,")
        File.write("Discription,")
        File.write("Images Addresses,")
        File.write("URL,\n")
  
    # specifying user agent, You can use other user agents
    # available on the internet
    HEADERS = ({'User-Agent':
                'Mozilla/4.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                                'Accept-Language': 'en-US, en;q=0.5'})
  
    # Making the HTTP Request
    webpage = requests.get(URL, headers=HEADERS)
  
    # Creating the Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "lxml")
   # print(soup)
   
    # print(soup)
    # retreiving product title
    try:
        # Outer Tag Object
        title = soup.find("span", 
                          attrs={"id": 'productTitle'})
  
        # Inner NavigableString Object
        title_value = title.string
  
        # Title as a string value
        title_string = title_value.strip().replace(',', '')
  
    except AttributeError:
        title_string = None
    # print("product Title = ", title_string)
  
    # saving the title in the file
    
    File.write(f"{title_string},")
  
    # retreiving price
    try:
        price = soup.find(
            "span", attrs={'id': 'priceblock_ourprice'}).string.strip().replace(',', '')

         
        # we are omitting unnecessary spaces
        # and commas form our string
    except AttributeError:
        price = None
    
    
    try:
     htmltable = soup.find('table', { 'class' : 'a-normal a-spacing-micro' })
    #  print(htmltable)
     def tableDataText(table):    
      """Parses a html segment started with tag <table> followed 
      by multiple <tr> (table rows) and inner <td> (table data) tags. 
      It returns a list of rows with inner columns. 
      Accepts only one <th> (table header/data) in the first row.
      """
      def rowgetDataText(tr, coltag='td'): # td (data) or th (header)       
        return [td.get_text(strip=True) for td in tr.find_all(coltag)]  
      rows = []
      trs = table.find_all('tr')
      headerow = rowgetDataText(trs[0], 'th')
      if headerow: # if there is a header row include first
        rows.append(headerow)
        trs = trs[1:]
      for tr in trs: # for every table row
        rows.append(rowgetDataText(tr, 'td') ) # data row       
      return rows

    
     list_table = tableDataText(htmltable)
     dict_table = {}
     for item_list in list_table:
        dict_table[item_list[0]]= item_list[1]


    except:
        dict_table={}
    

    File.write(f"{price},")
  
    # retreiving product rating
    try:
        rating = soup.find("i", attrs={
                           'class': 'a-icon a-icon-star a-star-4-5'}).string.strip().replace(',', '')
  
    except AttributeError:
  
        try:
            rating = soup.find(
                "span", attrs={'class': 'a-icon-alt'}).string.strip().replace(',', '')
        except:
            rating = None

    File.write(f"{rating},")
  
    try:
        review_count = soup.find(
            "span", attrs={'id': 'acrCustomerReviewText'}).string.strip().replace(',', '')
  
    except AttributeError:
        review_count = None

    File.write(f"{review_count},")
  

    try:
        available = soup.find("div", attrs={'id': 'availability'})
        available = available.find("span").string.strip().replace(',', '')
  
    except AttributeError:
        available = None

    File.write(f"{available},")



    myv = dict_table.get('Material')
    File.write(f"{myv},")
    myv = dict_table.get('Color')
    File.write(f"{myv},")
    myv = dict_table.get('Style')
    File.write(f"{myv},")
    myv = dict_table.get('Brand')
    File.write(f"{myv},")
    myv = dict_table.get('Product Dimensions')
    if myv != None:
       myv =myv.split(';')[0]
    File.write(f"{myv},")
    myv = dict_table.get('Pattern')
    File.write(f"{myv},")
    myv = dict_table.get('Product Dimensions')
    if myv != None:
      myv= myv.split(';')[1]
    File.write(f"{myv},")
    myv = dict_table.get('Age Range (Description)')
    File.write(f"{myv},")
    myv = dict_table.get('Capacity')
    File.write(f"{myv},")

    try:
     w3schollsList = soup.find("div", attrs={'id': 'featurebullets_feature_div'})
    

     updated_list = w3schollsList.find_all("span", attrs={'class': 'a-list-item'})

    # print(ulist)

     disc_list = ''
    #  str1= ''
    #  str1.replace('\', new)

     for span in updated_list:
        disc_list=disc_list+span.text.replace('\n', '-------').replace(',', '')

    #  print(disc_list)

    except:
     disc_list = None

    File.write(f"{disc_list},")
    



    # try:
    image_container = soup.find("div", attrs= {'id': 'imageBlock'})

    image_urls = image_container.find_all('img')
    
    image_urls_list = []
    
    for img in image_urls:
      if img.has_attr('src'):
        image_urls_list.append(img['src'])

    
    # print(image_urls_list)

    image_urls_list_string = "-------".join(image_urls_list)
    File.write(f"{image_urls_list_string},")

    # print(image_urls_list_string)

    

    File.write(f"{URL}")
    File.close()

    print(links_counter+1)
  
  
if __name__ == '__main__':
  # openning our url file to access URLs
    file = open("E:\\Visual Code Projects\\Python Projects\\file.txt", "r")
   
    counter = 0  
    for links in file.readlines():
        
        main(links, counter)
        counter = counter +1
      