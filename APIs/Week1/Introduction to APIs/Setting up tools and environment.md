<h1>Setting up tools and environment</h1>
<h2>Introduction</h2>
Before you can start an API project you need to have the right setup on your computer. In this reading, you will learn how to configure necessary extensions in VS Code. You will also learn how to use pipenv to manage the packages and the virtual environment for your API projects.

<h2>Step 1: Install VS Code</h2>
The previous reading guided you through installing Visual Studio code on your computer. This is the first step in setting up your development environment. If you have not installed it yet, go back to 
Installing VS Code
 and follow the steps.

<h2>Step 2: Install Pytho</h2>n
Download and install the latest version of Python from 
https://python.org
  or use the software manager for your operating system.

<h2>Step 3: Install the VS Code Python extension</h2>
Open VS code and access the extensions panel from the view menu, the left sidebar or by pressing Command, Shift and X. Search for Python and select the first one from Microsoft. This extension provides features like syntax highlighting, autosuggestions, debugging, and linting, which makes it very useful for Python developers.

<h2>Step 4: Install additional VS Code extensions (optional)</h2>
You can also install a few other useful VS Code extensions for Python development. Search for: Python Indent by Kevin Rose to correct Python indentation in VS Code, and Djaneiro by Scott Barkman for useful Django snippets.

<h2>Step 5: Install a package manager </h2>
Next, you need to install pipenv, a package manager for Python applications from 
https://pipenv.pypa.io/en/latest/ (https://pipenv.pypa.io/en/latest/)
. pipenv lets you easily create virtual environments for your projects so that you can manage your dependencies more efficiently. This allows you to install packages for your projects without conflicting with other versions of the same package used by other projects. 

To install pipenv, open your terminal or PowerShell and type the following command:

pip3 install pipenv
<img src='SUTAE_1'>

Type in pipenv and press enter. A list of commands and options supported by pipenv will display.

<img src='SUTAE_2'>

<h2>Conclusion</h2>
You should be set up to start your first Django API project using Python. You now know how to install the latest version of Python, the Python extension and other useful extensions in VS Code as well as the package manager pipenv.