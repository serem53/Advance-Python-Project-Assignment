from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import logging
logging.basicConfig(filename="scrapper.log" , level=logging.INFO)

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")

@app.route("/review" , methods = ['POST' , 'GET'])
def index():
    if request.method == 'POST':
        form_type = request.form['form_type']
        if form_type == 'jumia':
            try:
                print(request.form['content'])
                searchString = request.form['content'].replace(" ","")
                jumia_url = "https://www.jumia.co.ke/catalog/?q=" + searchString

                try:
                    response = requests.get(jumia_url)
                    response.raise_for_status() # Check for any HTTP request errors
                    print("request was successfull!")

                    # Parse the HTML content using BeautifulSoup
                    soup = bs(response.text,'html.parser')
                    # Now you can use 'soup' to extract data from the web page

                except requests.exceptions.RequestException as e:
                    #handle any request exceptions
                    print(f"request error: {e}")
                #handle any other exceptions
                except Exception as e:
                    print(f"an error occured: {e}")

                
                bigbox = soup.find_all('a',{"class":"core"})
                print(len(bigbox))

                reviews = []

                
                for i in bigbox:
                    product_req = requests.get("https://www.jumia.co.ke"+i.get('href'))
                    product_html = bs(product_req.text, 'html.parser')
                    product_box = product_html.find_all('article',{'class': '-pvs -hr _bet'})
                    for c in product_box:
                        try:
                            name = product_html.find('h1',{'class':'-fs20 -pts -pbxs'}).text
                            
                        
                        except:
                            name = 'No name'
                        


                        try:
                            rating = c.find('div',{'class':'stars _m _al -mvs'}).text
                        except:
                            rating = 'No Rating'
                            

                        try:
                            comments = [c.find('h3',  class_="-m -fs16 -pvs").text,c.find('p',  class_="-pvs").text]
                        except:
                            comments = 'No Comments'
                            

                        
                        mydict = {"Product": searchString, "Name": name, "Rating": rating, "Comments": comments}
                        
                        reviews.append(mydict)

                logging.info("log my final result {}".format(reviews))
                return render_template('result.html', reviews=reviews)
            except Exception as e:
                    logging.info(e)
                    return 'something is wrong'
            
        elif form_type == 'github':
            try:
                print(request.form['content'])
                searchString = request.form['content'].replace(" ","")
                github_url = "https://github.com/" + searchString

                try:
                    response = requests.get(github_url)
                    response.raise_for_status() # Check for any HTTP request errors
                    print("request was successfull!")

                    # Parse the HTML content using BeautifulSoup
                    soup = bs(response.text,'html.parser')
                    # Now you can use 'soup' to extract data from the web page
                
                except requests.exceptions.RequestException as e:
                    #handle any request exceptions
                    print(f"request error: {e}")
                #handle any other exceptions
                except Exception as e:
                    print(f"an error occured: {e}")
                    return f"could not find the username{searchString}"

                reviews = []
                github_name = soup.find('span',{"class":"p-name vcard-fullname d-block overflow-hidden"}).text
                
                
                try:
                    article = soup.find('div',{"class":"p-note user-profile-bio mb-3 js-user-profile-bio f4"}).text
                except:
                    article = 'not available'

                repo = requests.get(github_url+'?tab=repositories')
                repo.raise_for_status() # Check for any HTTP request errors
                print("request was successfull!")
                bsrepo = bs(repo.text,'html.parser')
                
                try:
                    repositories = bsrepo.find_all('h3',{"class":"wb-break-all"})
                except:
                    repositories = 'could not find any repositories'
                links = []
                for repo in repositories:
                    link = repo.find('a').attrs['href']
                    links.append(link)
                    print(link)
                

                        
                       
                my_dict={'name':github_name,'repositories':links,'article': article}     
                reviews.append(my_dict)

                logging.info("log my final result {}".format(reviews))
                return render_template('github.html', reviews=reviews)
            except Exception as e:
                    logging.info(e)
                    return f'could not find the github account associated with the userame {searchString},please check again'
        
        else:
                try:
                    print(request.form['content'])
                    searchString = request.form['content'].replace(" ","")
                    amazon_url = "https://www.amazon.com/s?k=" + searchString

                    try:
                        response = requests.get(amazon_url)
                        response.raise_for_status() # Check for any HTTP request errors
                        print("request was successfull!")

                        # Parse the HTML content using BeautifulSoup
                        soup = bs(response.text,'html.parser')
                        # Now you can use 'soup' to extract data from the web page

                    except requests.exceptions.RequestException as e:
                        #handle any request exceptions
                        print(f"request error: {e}")
                    #handle any other exceptions
                    except Exception as e:
                        print(f"an error occured: {e}")

                    
                    bigbox = soup.find_all('a',{"class":"a-link-normal s-no-outline"})
                    print(len(bigbox))

                    reviews = []

                    
                    for i in bigbox:
                        product_req = requests.get("https://www.amazon.com/"+i.get('href'))
                        product_html = bs(product_req.text, 'html.parser')
                        product_name = product_html.find('span',{'class':'a-size-large product-title-word-break'}).text
                        
                        product_rating = product_html.find('i',{'class':'a-icon a-icon-star a-star-4-5 cm-cr-review-stars-spacing-big'}).text
                        
                        comments = []
                        product_comment =product_html.find_all('div',{'class':'a-row a-spacing-small review-data'})
                        
                        for i in product_comment:
                            comments.append(i.text)
                        
                        
                                

                            
                        mydict = {"Product": product_name, "product_rating": product_rating, "Comments": comments}
                            
                        reviews.append(mydict)

                    logging.info("log my final result {}".format(reviews))
                    return render_template('amazon.html', reviews=reviews)
                except Exception as e:
                        logging.info(e)
                        return 'something is wrong'
        
    else:
        return render_template('index.html')


if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0")



            
            
           
          

    