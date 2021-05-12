from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import Select

def getfastaseq(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        file = f.read()
        fasta = {}
        for line in file.split("\n"):
            if line.startswith(">"):
                sequence_name = line.rstrip('\n').replace(">", "")
                continue
            else:
                sequence = line.rstrip('\n')
            if sequence_name not in fasta:
                fasta[sequence_name] = ''
            fasta[sequence_name] = fasta[sequence_name] + sequence
        return fasta

#需要传入使用的内切酶
def fuckCEDesign(fastadic,enzymeA,enzymeB):
    base_url = 'https://crm.vazyme.com/cetool/simple.html'
    f = open('result.txt','a')

    chrome_options = Options()
    chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"')
    chrome_options.add_argument("--headless")
    # 对应的chromedriver的放置目录
    driver = webdriver.Chrome(executable_path=(r'D:\GitRepository\EnzymeCutPrimerDesign\chromedriver.exe'), options=chrome_options)
    driver.implicitly_wait(10)
    driver.get(base_url)
    for seqname in fastadic.keys():
        
        #f.write(seqname+'\n')
        print(seqname+' begin!')
        seq = fastadic[seqname]

        time.sleep(1)

        driver.find_element_by_xpath('/html/body/div/form/div[1]/textarea').clear()
        driver.find_element_by_xpath('/html/body/div/form/div[1]/textarea').send_keys(seq)
        driver.find_element_by_xpath('/html/body/div/form/div[1]/div/div/label[2]/input').click()
        time.sleep(3)

        left_enz = Select(driver.find_element_by_xpath('/html/body/div/form/div[2]/div[1]/select[1]'))
        left_enz.select_by_visible_text(enzymeA)
        right_enz = Select(driver.find_element_by_xpath('/html/body/div/form/div[2]/div[1]/select[2]'))
        right_enz.select_by_visible_text(enzymeB)

        driver.find_element_by_xpath('/html/body/div/form/div[2]/div[2]/button[1]').click()

        time.sleep(3)

        leftprimer = driver.find_element_by_xpath('/html/body/div/form/div[2]/div[3]/div[1]/span[2]').text
        rightprimer = driver.find_element_by_xpath('/html/body/div/form/div[2]/div[3]/div[2]/span[2]').text
        
        f.write('{}-{}-left\t{}\n'.format(seqname,enzymeA,leftprimer))
        f.write('{}-{}-right\t{}\n'.format(seqname,enzymeB,rightprimer))
        print(seqname+' finished!')

    driver.close()
    f.close()

if __name__ == '__main__':
    genelist = getfastaseq('gene.txt')
    fuckCEDesign(genelist,'BamHI','SalI')