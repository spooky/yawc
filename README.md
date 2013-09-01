# Yet Another Webgen Clone

## Requirements
Requirements are listed in requirements.txt file. 
The easiest way to installis to run the following pip command:

    pip install -r requirements.txt

## Usage
There are few rules that you need to know to use yawc

* the website you want to generate needs it's own python package
* the package needs a 'content' module where you'll keep your...content
* templates are located in the 'templates' folder of your package
    * templates with a name starting with "_" are ignored during site generation - use these as master(ish) templates that can be extended on you page templates
* static files are located in the 'static' folder or your package
* use caution when creating links to interal pages. If the link is intended to stay on more than one page (like navigation), then using a full path is required (so something that starts at the root of your page - '/')

When you have a proper package structure, all you need to do is execute the script

    python yawc.py <package name> [<output dir>]

## Content
Content is the key element on a page so arange it wisely. The content directory structure will be reflected in your sites urls, so when trying to figure out the structure for your content - think 'sitemap'.

## Directory structure
You need to create a python package with the following structure:

* &lt;package_name&gt;
* \__init.py__ (empty)
* content
	* \__init__.py (your root page content)
	* foo.py (/foo content)
	* bar
		* \__init__.py (/bar content)
		* <bar static files> (images specific to /bar)
* static (static files - css, js, images)
* templates (jinja templates)
	* index.html

## Templates
[Jinja2](http://http://jinja.pocoo.org/) is used as a template engine. The default template name is 'index.html'. The directory structure should mirror content structure. If the structures don't match, the script will try to find a fallback template.
That means that if you have a module named foo.bar.buz, first the foo/bar/buz location will be searched, then the engine will look for a template in each of the paths parents, until it reaches the root template folder.
