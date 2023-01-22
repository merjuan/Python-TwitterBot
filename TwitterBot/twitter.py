from twitterInfo import username, password
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


class Twitter:
    def __init__(self,username,password):
        self.username=username
        self.password=password
        self.browserProfile=webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option('prefs',{'intl.accept_languages':'en,en_US'})
        self.browser=webdriver.Chrome('chromedriver.exe',chrome_options=self.browserProfile)

    def signIn(self):
        self.browser.get("https://twitter.com/i/flow/login")
        time.sleep(2)

        usernameInput=self.browser.find_element(By.XPATH,"//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input")
        usernameInput.send_keys(self.username)
        time.sleep(2)

        btnNext =self.browser.find_element(By.XPATH,"//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]")
        btnNext.click()
        time.sleep(2)

        passwordInput=self.browser.find_element(By.XPATH,"//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div/label/div/div[2]/div[1]/input")
        passwordInput.send_keys(self.password)

        btnLogin=self.browser.find_element(By.XPATH,"//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div")
        btnLogin.click()
        time.sleep(5)

    def search(self,hashtag):
        
        searchInput=self.browser.find_element(By.XPATH,"//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input")
        searchInput.send_keys(hashtag)
        time.sleep(5)
        searchInput.send_keys(Keys.ENTER)
        time.sleep(5)
        ##aşağıdaki işlem scroll aşağıya kaydıkça önceki tweetlerin silinip yerıne en yeni tweetlerin gösterilmesi.
        # bunun için ilk olarak bir liste tanımlayıp bu ilk tweetlerin saklanmasını sağlamak 

        results=[]
        list=self.browser.find_elements(By.XPATH,"//div[@data-testid='tweetText']")
        time.sleep(3)
        print("count: "+ str(len(list)))

        for i in list:
            results.append(i.text)




        loopCounter=0
        last_height=self.browser.execute_script("return document.documentElement.scrollHeight")##scroll u indirmek için gereklı olan javascript kodu    
        while True:
            if loopCounter>3: ##scrollu sınırlandırmak için.
                break
            self.browser.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
            time.sleep(5)
            new_hight=self.browser.execute_script("return document.documentElement.scrollHeight")
            if last_height==new_hight:
                break
            last_height=new_hight ##en son aldığımız yükseklik last_high olarak gelmesi için.
            loopCounter+=1
            list=self.browser.find_elements(By.XPATH,"//div[@data-testid='tweetText']")
            time.sleep(3)
            print("count: "+ str(len(list)))
            
            for i in list:
                results.append(i.text)

            count=1
            with open("tweets.txt","w",encoding="UTF-8") as file:
                for item in results:
                    file.write(f"{count}-{item}\n")
                    count +=1 

        # list=self.browser.find_elements(By.XPATH,"//div[@data-testid='tweetText']")   #####Bu kısmı almanın bir mantığı yok aynı divler kullanılıyor.
        # time.sleep(3)
        # print("count: "+ str(len(list)))
        

        ''' ###terminale yazdırmak yerine dosyaya yazmak daha iyi 
        count=1
        for item in results:
            print(f"{count}-{item}")
            count +=1
            print("*********")
        '''

            










twitter=Twitter(username,password)
twitter.signIn()
twitter.search('python')