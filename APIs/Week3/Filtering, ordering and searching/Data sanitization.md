<h1>Data sanitization</h1>

<h2>Introduction</h2>
Sanitization is the process of cleaning data from potential threats. Without proper sanitization, your API project can be exploited using common attacks like SQL injection. Additionally, client applications can suffer attacks like cross-site scripting or session hijacking via injecting JavaScript. For such cases, doing data validation is not enough. While Django performs different types of sanitization behind the scenes, you can set in motion additional sanitization processes to meet project-specific requirements. 

In this reading, you will learn how to avoid script injection and SQL Injection using data sanitization techniques in DRF.

<h2>Sanitize HTML and JavaScript </h2>
Unless it is intended, you should always check if the user client added an HTML tag inside the data and neutralized it by converting special HTML characters into HTML entities. This is because hackers can use <script> tags to inject JavaScript and <img> tags to add unwanted trackers. 

Imagine someone inputs Tomato Pasta <script>alert(‘hello’)</script> as a menu item. If you don’t sanitize the data, the script tag will successfully execute when you display this menu title. Attackers can inject malicious scripts in this way. An alert like (‘hello’) cannot do any harm, but attackers can inject malicious code which can be harmful. 

There is a popular third-party package called bleach that can help you to clean this. It will convert all HTML special characters like <’, ‘> and other tags to HTML entities so that the browser doesn’t execute them as HTML anymore. 

<b>Install bleach</b>
<b>Step 1</b>
Install the bleach package using pipenv first.

pipenv install bleach

<b>Step 2</b>
Import the bleach module in the serializers.py file. 

import bleach

<b>Step 3</b>
Sanitize the field data using both the validate_field() and validate() methods. Inside these validation methods, you have to use the clean() function provided by the bleach module to clean up the input data. 

To sanitize the title field, write a validate_title() method above the Meta class in the MenuItemSerializer.

def validate_title(self, value):
        return bleach.clean(value)

<b>Test it</b>
If you send a POST request to the menu-items endpoint with HTML tags in the title field, the input data submitted by the client or user will be sanitized properly. Note how the script tag has been converted to HTML entities in the screenshot below.

<img src='DS_1.png'>

Without sanitization, the input data will be saved in the database as it was submitted.

<img src='DS_2.png'>

You can also sanitize the title field inside the validate method using this line of code.

attrs['title'] = bleach.clean(attrs['title'])

This way, you can sanitize multiple fields from one single place. Here is the complete validate() method inside the MenuItemSerializer.

<img src='DS_3.png'>

<h2>Preventing SQL injection</h2>
SQL injection is commonly used by attackers by injecting SQL queries in the input data to perform malicious actions in the database.

Preventing SQL injection is comparatively easy. Although it is usually not advisable to run raw SQL there are cases where it’s necessary. Still, if you really need to run raw SQL, you must escape the parameters using string placeholders.  You should never keep the placeholder inside quotations because then you will be at risk of SQL injection. Below are one correct and two incorrect examples of preventing SQL injection.

Note: Always avoid running raw SQL queries unless it is absolutely necessary. 

<b>Correct way: Using parameterized query and no quotation</b>

limit = request.GET.get(‘limit’)
MenuItem.objects.raw('SELECT * FROM LittleLemonAPI_menuitem LIMIT %s', [limit]) 

<b>Incorrect: Using string formatting</b>

limit = request.GET.get(‘limit’)
MenuItem.objects.raw('SELECT * FROM LittleLemonAPI_menuitem LIMIT %s' % limit)

<b>Incorrect: Using a string placeholder inside quotation</b>

limit = request.GET.get(‘limit’) 
MenuItem.objects.raw(“SELECT * FROM LittleLemonAPI_menuitem LIMIT ‘%s' “, [limit])

<h2>Conclusion </h2>
In this reading, you learned that it is important to sanitize data to protect data from potential threats such as script injection and SQL injection. You now know about a few practical ways to sanitize your data in DRF.