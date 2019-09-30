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

    print("||  IP#  |                Location                  |                             IP Address                            |    Runtime   ||")
    print("||_______|__________________________________________|___________________________________________________________________|______________||")

    total_start = time.time()
    min = ''
    minTime = 100
    max = ''
    maxTime = 0
    j = 1
    for i in data['addresses']:

        try:
            location = i[0:i.find("@")]
            ip = i[i.find("@")+1:len(i)]
            if ip[0] != 'h':
                ip = 'http://' + ip

            ## Step through each IP Address recording Time
            start = time.time()

            res = requests.get(ip)

            ## Get and Print the Random Number
            result = res.text[(res.text.find("<h1>")+1):(res.text.find("</h1>")+1)]

            finish = time.time()
            print("|| %5d | %40s | %65s | %12.7f ||" %(j, location, ip, (finish - start)))
            if (finish - start) < minTime:
                minTime = finish - start
                min = "|| %5d | %40s | %65s | %12.7f ||" %(j, location, ip, (finish - start))
            if (finish - start) > maxTime:
                maxTime = finish - start
                max = "|| %5d | %40s | %65s | %12.7f ||" %(j, location, ip, (finish - start))
        except:
            print("|| %5d |------------------------------------------|----------------------ERROR-CAUGHT---------------------------------|--------------||" %(j))
        j = j + 1

    total_finish = time.time()
    print()
    print("Maximum:\n %s" %max)
    print("Minimum:\n %s" %min)
    print()
    print('Total Runtime of the Program is ' + str(total_finish - total_start) + ' seconds')
