import requests
import re
import yaml
import time
import socket

if __name__ == "__main__":
    ## Request HTML text from Database Page and Load in YAML
    res = requests.get('https://masonschmidt.github.io/SoftEngProj1/')
    yamlfile = res.text[res.text.find("<pre>")+1:res.text.find("</pre>")]

    ## Use YAML library to parse the YAML into an object
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)

    ## Start time of full program
    total_start = time.time()

    ## IP address of Working Instance
    IPAddr = socket.gethostbyname(socket.gethostname() )

    ## Loop through addresses in yaml
    for i in data['addresses']:

        ## Get location
        location = i[0:i.find("@")]

        ## Get url
        ip = i[i.find("@")+1:len(i)]
        if ip[0] != 'h':
            ip = 'http://' + ip

        try:
            ## Step through each IP Address recording Time
            start = time.time()

            ## Get info from page
            res = requests.get(ip)

            ## Get and Print the Random Number
            result = re.findall('\d+', res.text )

            ## Get time taken to search url
            finish = time.time()

            ## Print Results
            print("%s:%s@%s %.7f %d" %(IPAddr, location, ip, (finish - start), int(result[0])))

        except: ## Catch Exceptions
            print("----------ERROR-CAUGHT-----------")

    ## Final Time
    total_finish = time.time()

    ## Print final time
    print('Total Runtime of the Program is ' + str(total_finish - total_start) + ' seconds')
