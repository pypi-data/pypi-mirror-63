# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neattext']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'neattext',
    'version': '0.0.1',
    'description': 'Neattext - a simple NLP package for cleaning text',
    'long_description': '# neattext\nNeatText a simple NLP package for cleaning textual data and text preprocessing\n\n\n#### Problem\n+ Cleaning of unstructured text data\n+ Reduce noise [special characters,stopwords]\n+ Reducing repetition of using the same code for text preprocessing\n\n#### Solution\n+ convert the already known solution for cleaning text into a reuseable package\n\n\n#### Installation\n```bash\npip install neattext\n```\n\n### Usage\n#### Clean Text\n+ Clean text by removing emails,numbers,stopwords,etc\n```python\n>>> from neattext import TextCleaner\n>>> docx = TextCleaner()\n>>> docx.text = "your text goes here"\n>>> docx.clean_text()\n```\n\n#### Remove Emails,Numbers,Phone Numbers \n```python\n>>> docx.remove_emails()\n>>> docx.remove_numbers()\n>>> docx.remove_phone_numbers()\n>>> docx.remove_stopwords()\n```\n\n\n#### Remove Special Characters\n```python\n>>> docx.remove_special_characters()\n```\n\n#### Replace Emails,Numbers,Phone Numbers\n```python\n>>> docx.replace_emails()\n>>> docx.replace_numbers()\n>>> docx.replace_phone_numbers()\n```\n\n### Using TextExtractor\n+ To Extract emails,phone numbers,numbers from text\n```python\n>>> from neattext import TextExtractor\n>>> docx = TextExtractor()\n>>> docx.text = "your text with example@gmail.com goes here"\n>>> docx.extract_emails()\n```\n\n\n### More Features To Add\n+ unicode explainer\n+ currency normalizer\n\n\n#### By \n+ Jesse E.Agbe(JCharis)\n+ Jesus Saves @JCharisTech\n\n\n\n#### NB\n+ Contributions Are Welcomed\n+ Notice a bug, please let us know.\n+ Thanks A lot\n',
    'author': 'Jesse E.Agbe(JCharis)',
    'author_email': 'jcharistech@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Jcharis/neattext',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
