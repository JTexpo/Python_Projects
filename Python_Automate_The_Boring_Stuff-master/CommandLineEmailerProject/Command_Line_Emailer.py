from selenium import webdriver
import json
import time
import sys, os


def get_all_info():
    my_dic = json.load(open("Gmail_Automation_Info.txt",'r'))
    return my_dic["Gmail"],my_dic["Password"],my_dic["Send_to"],my_dic["Subject"],my_dic["Message"]
    

if __name__ == "__main__":
    pathname = os.path.dirname(sys.argv[0])

    username,password,send_to,sub,msg = get_all_info()
    
    browser = webdriver.Firefox(executable_path=pathname+'/geckodriver')
    # Get The Login Page
    browser.get('https://accounts.google.com/signin/v2/identifier?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com%2Fsearch%3Fclient%3Dfirefox-b-1-d%26q%3Dgoogle%2Bgmail&flowName=GlifWebSignIn&flowEntry=ServiceLogin')
    # Get UserName Textbox
    browser.find_element_by_xpath('//*[@id="identifierId"]').send_keys(username)
    # Get The Submit Button
    browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/span/span').click()
    # Waiting For The Page To Refresh
    while not (browser.current_url in "https://accounts.google.com/signin/v2/sl/pwd?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com%2Fsearch%3Fclient%3Dfirefox-b-1-d%26q%3Dgoogle%2Bgmail&flowName=GlifWebSignIn&flowEntry=ServiceLogin&cid=1&navigationDirection=forward"):
        continue
    time.sleep(1)
    # Get Password Textbox
    browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input').send_keys(password)
    # Get The Submit Button
    browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/span/span').click()
    
    browser.get("https://mail.google.com/mail/u/0/#inbox?")
    time.sleep(1)
    # Get The Compose Button
    browser.find_element_by_xpath('/html/body/div[7]/div[3]/div/div[2]/div[1]/div[1]/div[1]/div/div/div/div[1]/div/div').click()
    # Waiting For The Page To Refresh
    while not ("https://mail.google.com/mail/u/0/#inbox?compose=new" in browser.current_url):
        continue
    time.sleep(1)
    # Get The To Textbox
    browser.find_element_by_xpath('//*[@id=":pk"]').send_keys(send_to)
    # Get The Subjuct Textbox
    browser.find_element_by_xpath('//*[@id=":p2"]').send_keys(sub)
    # Get The Message Textbox
    browser.find_element_by_xpath('//*[@id=":q7"]').send_keys(msg)
    # Get The Send Button
    browser.find_element_by_xpath('//*[@id=":os"]').click()
