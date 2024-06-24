METADATA =\
{
	'name': 'LiveStream-AI',
	'description': 'Next generation face swapper and enhancer',
	'version': '2.6.0',
	'license': 'MIT',
	'author': 'Henry Ruhs',
	'url': 'https://livestream.ai'
}


def get(key : str) -> str:
	return METADATA[key]
