import requests
import re
import yaml
import time

if __name__ == "__main__":
    ## Request HTML text from Database Page and Load in YAML
    res = requests.get('https://masonschmidt.github.io/SoftEngProj1/')
    yamlfile = res.text[res.text.find("<pre>")+1:res.text.find("</pre>")]

    ## Use YAML library to parse the YAML into an object
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)

    print("||         Location          |                     IP Address                     |     Runtime     ||")
    print("------------------------------------------------------------------------------------------------------")

    total_start = time.time()

    for i in data['addresses']:

        location = i[0:i.find("@")]
        ip = i[i.find("@")+1:len(i)]

        ## Step through each IP Address recording Time
        start = time.time()

        res = requests.get(ip)

        ## Get and Print the Random Number
        result = res.text[(res.text.find("<h1>")+1):(res.text.find("</h1>")+1)]

        finish = time.time()
        print("|| %25s | %50s | %15.7f ||" %(location, ip, ((finish - start)/1000)))


    total_finish = time.time()
    print('Total Runtime of the Program is ' + str((total_finish - total_start)/1000) + ' seconds')
