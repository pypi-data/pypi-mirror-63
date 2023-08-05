#  robotframework-dictkeyallpaths Library

robot framework - To get all paths of dictionary

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install robotframework-dictkeyallpaths.

```bash
pip install robotframework-dictkeyallpaths
```

## Usage

```python
# - Example:
#json_string as below:
{
	  	"SuperMarket": {
		    "Fruit": [
		      {
		        "Name": "Apple",
		        "Manufactured":"USA",
		        "price": 7.99
		      },
		      {
		        "Name": "Banana",
		        "Manufactured":"Japan",
		        "price": 3.99
		      }
		    ],
		    "Drink": {
				"SoftDrink":{
					"Cola": [
				      	{
				      		"Color":"Red",
				      		"Price":15.00
				      	},
				      	{
				      		"Color":"Green",
				      		"Price":17.99
				      	}
				      ],      
				      "Coffee": {
				      	"Hot":[
					      	{
					      		"Type":"Espresso",
					      		"Price":15.90
					      	},
					      	{
					      		"Type":"Cappuccino",
					      		"Price":10.90
					      	}
					    ],
					    "Ice":[
					      	{
					      		"Type":"Espresso",
					      		"Price":20.90
					      	},
					      	{
					      		"Type":"Cappuccino",
					      		"Price":15.90
					      	}
					    ]
				    }
				}     
		    }
	  	}
	}


# - How to use keyword in robotframework
Test case get all paths of dictionary
    ${dictData}=    Evaluate    json.loads("""${json_string}""")    json
    :FOR    ${item}    IN    @{allJsonKeys}
        Log To Console    key:${item} >> value:${dictData${item}}
    END


# - Console display
key:['SuperMarket']['Fruit'][0]['Name'] >> value:Apple
key:['SuperMarket']['Fruit'][0]['Manufactured'] >> value:USA
key:['SuperMarket']['Fruit'][0]['price'] >> value:7.99
key:['SuperMarket']['Fruit'][1]['Name'] >> value:Banana
key:['SuperMarket']['Fruit'][1]['Manufactured'] >> value:Japan
key:['SuperMarket']['Fruit'][1]['price'] >> value:3.99
key:['SuperMarket']['Drink']['SoftDrink']['Cola'][0]['Color'] >> value:Red
key:['SuperMarket']['Drink']['SoftDrink']['Cola'][0]['Price'] >> value:15.00
key:['SuperMarket']['Drink']['SoftDrink']['Cola'][1]['Color'] >> value:Green
key:['SuperMarket']['Drink']['SoftDrink']['Cola'][1]['Price'] >> value:17.99
key:['SuperMarket']['Drink']['SoftDrink']['Coffee']['Hot'][0]['Type'] >> value:Espresso
key:['SuperMarket']['Drink']['SoftDrink']['Coffee']['Hot'][0]['Price'] >> value:20.90
key:['SuperMarket']['Drink']['SoftDrink']['Coffee']['Hot'][1]['Type'] >> value:Cappuccino
key:['SuperMarket']['Drink']['SoftDrink']['Coffee']['Hot'][1]['Price'] >> value:10.90
key:['SuperMarket']['Drink']['SoftDrink']['Coffee']['Ice'][0]['Type'] >> value:Espresso
key:['SuperMarket']['Drink']['SoftDrink']['Coffee']['Ice'][0]['Price'] >> value:20.90
key:['SuperMarket']['Drink']['SoftDrink']['Coffee']['Ice'][1]['Type'] >> value:Cappuccino
key:['SuperMarket']['Drink']['SoftDrink']['Coffee']['Ice'][1]['Price'] >> value:15.90
```

## Contributing
I will continue to develop to make it more complete.

Best Regards,  
Yoochar

## License
[MIT](https://choosealicense.com/licenses/mit/)