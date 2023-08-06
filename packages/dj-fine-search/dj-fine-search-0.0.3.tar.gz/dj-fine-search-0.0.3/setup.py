import setuptools

long_description = """
# Django Fine Search

https://github.com/bellomusodiq/dj-fine-search


Django fine search is package that performs search based on keywords. It allows word flexibility
for performing filter in a queryset. 
e.g. The native Model.object.filter(title__icontains='hello world') will return queryset of 
objects that contains substring "hello world", if the "world" comes before the "hello", the 
objects would not be found. Django fine search improves that, Django fine search will include
all objects that has substring "hello world".

```
class MyModel(models.Model):    
    title = models.Charfield(max_length=200)
    text = models.TextField()
    ...
```



perform_search takes in the model, search_text and fields

model: Model class, the model to perform filter on

search_text: string, the query that will be used for the filtering

fields: list or tuple of the fields of the models that the search will be performed on e.g. title and text above

perform_search function returns a list of model objects

```
from django_fine_search import perform_search
queryset = perform_search(model=MyModel, search_text='hello world', fields=["title", "text"])
```

assume we have the queryset below are result of MyModel.objects.all()
queryset = [{"id": 1, "title": "some title", "text": "hello world, how are you"},
            {"id": 2, "title": "some title2", "text": "the world is good"}, 
            {"id": 3, "title": "some title3", "text": "world hello there, hello"}] 

if we run perform_search on the MyModel with search_text='hello world' and fields=['title', 'fields']

it will return all the queries
"""

# with open("./README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="dj-fine-search",
    version="0.0.3",
    author="Mayowa Bello",
    author_email="bmayowa25@gmail.com",
    description="A key word based queryset search for django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bellomusodiq/dj-fine-search",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)