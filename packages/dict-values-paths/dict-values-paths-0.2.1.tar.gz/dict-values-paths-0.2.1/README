#  getDictAllPaths Library

python library - To get all paths and values of dictionary

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dict-values-paths.

```bash
pip install dict-values-paths
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


# - How to use function "getDictPaths" and "getDictValues"
	dictData=json.loads(json_string)
	dictKeys=GetDictAllPaths()
	keyList=dictKeys.getDictPaths(dictData)
	valueList=dictKeys.getDictValues(dictData)


# - Console display
[['SuperMarket', 'Fruit', '0', 'Name'], ['SuperMarket', 'Fruit', '0', 'Manufactured']
, ['SuperMarket', 'Fruit', '0', 'price'], ['SuperMarket', 'Fruit', '1', 'Name']
, ['SuperMarket', 'Fruit', '1', 'Manufactured'], ['SuperMarket', 'Fruit', '1', 'price']
, ['SuperMarket', 'Drink', 'SoftDrink', 'Cola', '0', 'Color'], ['SuperMarket', 'Drink', 'SoftDrink', 'Cola', '0', 'Price']
, ['SuperMarket', 'Drink', 'SoftDrink', 'Cola', '1', 'Color'], ['SuperMarket', 'Drink', 'SoftDrink', 'Cola', '1', 'Price']
, ['SuperMarket', 'Drink', 'SoftDrink', 'Coffee', 'Hot', '0', 'Type'], ['SuperMarket', 'Drink', 'SoftDrink', 'Coffee', 'Hot', '0', 'Price']
, ['SuperMarket', 'Drink', 'SoftDrink', 'Coffee', 'Hot', '1', 'Type'], ['SuperMarket', 'Drink', 'SoftDrink', 'Coffee', 'Hot', '1', 'Price']
, ['SuperMarket', 'Drink', 'SoftDrink', 'Coffee', 'Ice', '0', 'Type'], ['SuperMarket', 'Drink', 'SoftDrink', 'Coffee', 'Ice', '0', 'Price']
, ['SuperMarket', 'Drink', 'SoftDrink', 'Coffee', 'Ice', '1', 'Type'], ['SuperMarket', 'Drink', 'SoftDrink', 'Coffee', 'Ice', '1', 'Price']]
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
['Apple', 'USA', '7.99', 'Banana', 'Japan', '3.99', 'Red', '15.0', 'Green', '17.99', 'Espresso', '15.9', 'Cappuccino', '10.9', 'Espresso', '20.9', 'Cappuccino', '15.9']
```

## Contributing
I will continue to develop to make it more complete.

Best Regards,  
Yoochar

## License
[MIT](https://choosealicense.com/licenses/mit/)