import requests
import re
import yaml
import time

if __name__ == "__main__":
    ## Request HTML text from Database Page and Load in YAML
    res = requests.get('https://glen5641.github.io/YAMLEXAML/')
    yamlfile = res.text[res.text.find("<pre>")+5:res.text.find("</pre>")]

    ## Use YAML library to parse the YAML into an object
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)

    ## Step through each IP Address recording Time
    start = time.time()
    for i in data['ipaddresses']:
        res = requests.get(i)

        ## Get and Print the Random Number
        result = res.text[(res.text.find("<h1>")+4):(res.text.find("</h1>"))]
        print(i + " :: " + result)

    ## Collect final time in Milliseconds
    ## and print difference in seconds
    finish = time.time()
    print(str((finish - start)/1000) + ' seconds')
