#!/usr/bin/env python3

def get_site_config(): # All contents appear left to right in the final website
    return {
        'site_title': 'My Blog',
        'site_subtitle': 'A simple blog about various topics',
        'site_url': 'https://example.com',
        'header_links': [ # If you add or remove a entry here also add or remove the respective .md file in the pages directory and set the .html reference there to share the name of your .md name if you are adding one
            {'url': '/index.html', 'text': 'Home'}, # Don't Remove
            {'url': '/about.html', 'text': 'About'},
            {'url': '/contact.html', 'text': 'Contact'},
            {'url': '/archive.html', 'text': 'Archive'}, # Don't Remove
            {'url': '/tags.html', 'text': 'Tags'}, # Don't Remove
        ],
        'footer_links': [
            {'url': 'https://twitter.com/', 'text': 'Twitter'},
            {'url': 'https://github.com/', 'text': 'GitHub'},
            {'url': '/rss.xml', 'text': 'RSS'}, # Don't Remove
        ]
    }
    
# You actually can remove the entries marked with `# Don't Remove` and they will still generate but links to those pages wont appear in the header of footer anymore. 
