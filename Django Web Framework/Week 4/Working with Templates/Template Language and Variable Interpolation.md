<h1>Template Language and Variable Interpolation</h1>
In this reading, you will further explore the templating language and how it can be used to create markup. 

This reading will also showcase the use of variables and how they can be dynamically passed in a template to render out different content. 

Introduce learners to the template language with variables, filters and tags."

<h2>Template Engine</h2>
Modern web frameworks use a web template system to merge a data source with static HTML to generate dynamic web pages. 

A web template is an otherwise static HTML script interspersed with placeholder blocks of template language code. The template engine takes one set of data from any source, such as a database table, substitutes in placeholders and renders the generated content to the client browser.

<img src="TLVI1.png">

Django’s template engine uses its own Django Template Language. The default project template is configured that way. However, you may choose to use any other template language such as jinja2.

Django Template Language has three important components: variables, tags, and filters

<h2>Template variable</h2>
As you have previously learned, templates are HTML pages. The DIRS attribute of the TEMPLATES variable in the settings.py file points to the folder in which the templates are stored. Generally, the templates folder is in the root project folder.

The easiest way to display a template web page is by calling the render()function from within a view function. Its three parameters are the HTTP request object, the page itself, and a context dictionary.

Assuming that the client URL is 
http://localhost:8000/myapp/Novak
, the following view function receives the path parameter from the URL dispatcher and passes it as context to the template:

def index(request, name):       
    context={'name': name}   
    return render(request, 'index.html', context) 

<b>The keys in the context dictionary are available to the template as a variable. </b>

When put inside double curly brackets, the value is substituted at runtime. 

Put the following statement in the body of index.html.

<h2>Welcome {{ name }}</h2>

As a result, if the view receives Novak as the parameter, Hello Novak is rendered.

The value of any key in the context may be a singular object (string, integer), a list or a dictionary. 

A certain view passes a ‘person’ dictionary as a context.

person={'name':'Roger', 'profession':'Teacher'}} 
return render(request, 'person.html', person)	 

Inside the template, you can access the value associated with each key with the dot (".") operator just as the attributes of an object are used. For example:

Name: {{ person.name }} 
Profession: {{ person.profession }} 

This will render the following output on the browser.
<ul>
    <li> Name: Roger </li>
    <li> Profession: Teacher </li>
</ul>

<h2>Template tags</h2>
Just as there are HTML tags, the Django template language defines several tags. You can think of the tags as the keywords in a traditional programming language. You place the tags inside {% tag %} symbols. 

The if and for tags are important because they add processing logic to the web page.


<b>{% if %}</b>
With the if tag, the template variable is checked against a Boolean expression and a block of HTML is rendered conditionally.

{% if expression == True %} 
HTML block 1 
{% else %} 
HTML block 2 
{% endif %} 

Even though the syntax of if (and for) is very similar to Python, Django template language (DTL) doesn't use uniformly indented blocks. Hence, for every if tag, there is an endif tag.

A simple example of Django’s if tag is as follows:

The following view passes {'user':'admin'} dictionary as context to the template.

def index(request): 
    context={'user':'admin'} 
    return render(request, 'index.html', context) 

The conditional block in the template should be as follows:

{% if user == "admin" %} 
<h2>Welcome {{ user }}</h2> 
{% else %} 
<h2>Welcome Guest. You dont have admin access</h2> 
{% endif %} 


<b>{% for %}</b>
You can construct a looping construct inside the template with {% for %} and {% endfor %} tags. It is used to traverse any Python iterable such as a list, tuple or string.

In the following example, you pass a list to the template as its context.

def myview(request): 
    langs = ['Python', 'Java', 'PHP', 'Ruby', 'Rust'] 
    return render(request, 'langs.html', {'langs':langs}) 

Inside the template, the <b>for</b> loop is constructed, much like in Python to render the names of languages as unordered list.

<h1>List of Languages</h1> 
<ul> 
    {% for lang in langs %} 
    <li>{{ lang }}</li> 
    {% endfor %} 
</ul> 

If the value of a context variable is a dictionary, you can traverse the key–value pairs using the for syntax.

{% for key, value in data.items %} 
    {{ key }}: {{ value }} 
{% endfor %} 

<b>DTL has a number of helper variables to be used within the loop:</b>
forloop.counter: The current iteration of the loop

<ul> 
    {% for lang in langs %} 
    <li>{{ forloop.counter }} : {{ lang }}</li> 
    {% endfor %}  
</ul> 

Output:

List of Languages

1: Python

2: Java

3: PHP

4: Ruby

5: Rust

<b>forloop.revcounter</b>: The number of iterations from the end of the loop (1-indexed)

<ul> 
    {% for lang in langs %} 
    <li>{{ forloop.revcounter }} : {{ lang }}</li> 
    {% endfor %} 
  
</ul> 

Output:

List of Languages

5: Python

4: Java

3: PHP

2: Ruby

1: Rust

<b>forloop.first</b>: True if this is the first time through the loop

<ul> 
    {% for lang in langs %} 
    <li>{{ forloop.first }} : {{ lang }}</li> 
    {% endfor %} 
</ul> 

Output:

List of Languages

True: Python

False: Java

False: PHP

False: Ruby

False: Rust

<b>forloop.last</b>: True if this is the last time through the loop

<ul> 
    {% for lang in langs %} 
    <li>{{ forloop.last }} : {{ lang }}</li> 
    {% endfor %} 
</ul> 

Output:

List of Languages

False: Python

False: Java

False: PHP

False: Ruby

True: Rust

<b>forloop.parentloop</b>: For nested loops, this is the loop surrounding the current one. 

If you pass the following dictionary object as context:

dct = {'digits': ['One', 'Two', 'Three'],'tens': ['Ten', 'Twenty', 'Thirty']} 

The template has nested loops as follows:

<h1>Nested loops</h1> 

    {% for key, values in dct.items %} 
    <p>{{ forloop.parentloop.counter }}:{{ key }}</p> 
    <ul> 
    {% for value in values %} 
    <li> {{ value }}</li> 
    {% endfor %} 
</ul> 
{% endfor %} 

Output:

1:digits


One

Two

Three


2:tens


Ten

Twenty

Thirty

<b>{% comment %}</b>
Everything between {% comment %} and {% endcomment %} is ignored. An optional note may be inserted in the first tag.

{% comment "Optional note" %} 
    <p>Commented out text </p> 
{% endcomment %} 

<b>{% block %}</b>
Defines a block that can be overridden by child templates. This tag will be discussed when you learn about template inheritance.

<b>{% csrf_token %}</b>
This tag is used in a form template as protection to prevent Cross Site Request Forgeries (CSRF). This tag generates a token on the server-side to make sure to cross-check that the incoming requests do not contain the token. If found, they are not executed.


<b>{% include }%</b>
Loads a template and renders it with the current context. This is a way of "including" other templates within a template. The template name can either be a variable or a hard-coded (quoted) string, in either single or double quotes. 

{% include "sample.html" %} 

<b>{% with %}</b>
This tag sets a local variable that is available between {% with %}and {% endwidth %} tags.

{% with rate = 5 %} 
   Interest = {amt}*{{ rate }} 
{% endwith %} 

<h2>Filters</h2>
The filters modify the representation of the variable used in the template code. The modified value of the variable is rendered in the {{ }} tags. The filter is applied with the | (known as Pipe) symbol. The general form of using filter is:
{{ variable | filter_name }} 

<b>DTL has defined a number of filters. Here are some of the most frequently used:</b>

<h2>default</h2>
Django view passes a variable to the template. In the code below, value is a template variable. If it has been initialized in the view, it is set to the specified default, which in this case is nothing. 

{{ value|default:"nothing" }} 

If the value is an empty string, the output will be nothing.

<h2>join</h2>
This tag is similar to Python’s str.join(list) method. It joins the items in a list with the given separator. 

For example:

{{ words|join:" _ " }} 

If the view passes a list [' Django ', 'Template', 'Language'], the output will be the string "'Django_ Template_Language'".

<h2>length</h2>
When applied, this filter returns the length of the sequence received from the context. This works for both strings and lists.

{{ name|length }} 

If name is "John", the output will be 4. It returns 0 for an undefined variable.

<h2>first</h2>
Returns the first item in a list. Assuming that the list from the view function is ['a', 'b', 'c'].

{{ list|first }} 

The output will be 'a'.


<b>last</b>
If value is the list ['a', 'b', 'c', 'd'], the output will be the string "d".


<b>lower</b>
Converts a string into all lowercase.


<b></b>
upper converts a string into all uppercase.


<b>title</b>
title converts a string into title case by making words start with an uppercase character and the remaining characters lowercase.  

For example:

string = "django template language", the output will be "Django Template Language".

{{ string|title }} 

<b>length</b>
Returns the length of string or a list.

For the above string variable, the output will be 21.

{{ string|length }} 

<b>wordcount</b>
wordcount works on a string variable only and returns the number of words. For the above string variable, the output will be 3.

{{ string|wordcount }} 

In this reading, you explored the elements of Django Template Language, variables, tags and filters.