# Dummy Simple Blog Generator

A dummy-simple Python script that makes it very easy to create and maintain a static blog using markdown files. 
Once configured, making a new post is as simple as creating a new markdown file, writing your new post, and running the script.

# Features
- Completely static html design with zero JavaScript
- Tag system
- Post archive browser
- RSS.xml generation
- Formatting using markdown

## Installation

1. Clone the repository:
```
git clone https://github.com/VilktorK/DummySimpleBlogGenerator
```

2. Install Dependencies:
```
pip install markdown Jinja2
```

## Initial Setup

1. Configure config.py:
- Open `config.py` and modify the default settings:
```
  'site_title': 'Your Blog Title'
  'site_subtitle': 'Your Blog Subtitle'
  'site_url': 'https://yourdomain.com'
```

2. Configuring the header and footer
- The Home, Archive, and Tags pages are created automatically
- By default the only customizable pages are `about.md` and `contact.md` located in the pages directory
- To create more pages add a new `mynewpage.md` file to the pages directory with the same formatting as `about.md` and `contact.md `
- To this new page appear in the header, add a new entry to `config.py` like this:
```
            {'url': '/index.html', 'text': 'Home'},
            {'url': '/about.html', 'text': 'About'},
            {'url': '/mynewpage.html', 'text': 'My New Page'},
            {'url': '/contact.html', 'text': 'Contact'},
            {'url': '/archive.html', 'text': 'Archive'},
            {'url': '/tags.html', 'text': 'Tags'},
```
- The `mynewpage.md` will automatically become `mynewpage.html` when compiled
- New footer entries can be added the same way

## Regular Usage  

1. Making a new post
- Add a new post to the post directory like `postname.md` anytime you want to make a new post.
- A post must always use this header format for proper indexing:
```
---
title: My Blog Post Title
date: 2024-10-16
tags: [tagone, tagtwo, tagthree]
---
```

2. Compiling the site
- Simply run `generator.py` and your new blog will be generated in the output folder
- To add new posts or pages just add them to their corresponding folder and run `generator.py` again 

## Markdown Formatting
 - All formatting is handled by the "markdown" python library.
 - https://github.com/Python-Markdown/markdown

## TODO
 - Images do not yet scale with the page
