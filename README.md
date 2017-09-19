# charles_to_postman
Script for converting Charlesproxy output to a Postman json file

1) In Charlesproxy, choose File | Export Session...
2) Select the "JSON Session File" format
3) Use the resulting file as the input parameter for *charles\_to\_postman.py* 

```
 usage: charles_to_postman.py [-h] -i INPUT -o OUTPUT -n NAME
 
 Charlesproxy to Postman converter
 
 optional arguments:
   -h, --help            show this help message and exit
 
 required arguments:
   -i INPUT, --input INPUT
                         Input file in the *.chlsj format
   -o OUTPUT, --output OUTPUT
                         Output file
   -n NAME, --name NAME  Name of the target Postman collection```
