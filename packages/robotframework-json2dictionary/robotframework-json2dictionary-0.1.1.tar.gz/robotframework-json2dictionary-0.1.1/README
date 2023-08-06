#  JsonToDict Library

robot framework - To convert json to dictionary

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install robotframework-json2dictionary.

```bash
pip install robotframework-json2dictionary
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
${dataDict}=   Convert Json To Dictionary    ${json_string}


# - Console display
{'Fruit': [{'Name': 'Apple', 'Manufactured': 'USA', 'price': 7.99}
, {'Name': 'Banana', 'Manufactured': 'Japan', 'price': 3.99}]
, 'Drink': {'SoftDrink': {'Cola': [{'Color': 'Red', 'Price': 15.0}
, {'Color': 'Green', 'Price': 17.99}], 'Coffee': {'Hot': [{'Type': 'Espresso'
, 'Price': 15.9}, {'Type': 'Cappuccino', 'Price': 10.9}]
, 'Ice': [{'Type': 'Espresso', 'Price': 20.9}, {'Type': 'Cappuccino', 'Price': 15.9}]}}}}
```

## Contributing
I will continue to develop to make it more complete.

Best Regards,  
Yoochar

## License
[MIT](https://choosealicense.com/licenses/mit/)