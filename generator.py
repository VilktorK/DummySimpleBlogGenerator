#!/usr/bin/env python3
import os
import markdown
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from collections import defaultdict
import re
import xml.etree.ElementTree as ET
from email.utils import formatdate
import configparser
import shutil
from config import get_site_config

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader('templates'))

def parse_markdown(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
        # Replace image references
        content = re.sub(r'!\[([^\]]*)\]\(resources/([^\)]+)\)', r'![\1](/images/\2)', content)
        md = markdown.Markdown(extensions=['meta'])
        html = md.convert(content)
        return html, md.Meta

def parse_tags(tags_string):
    return [tag.strip() for tag in re.findall(r'[^,\[\]]+', tags_string)]

def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def copy_images():
    ensure_directory('output/images')
    if os.path.exists('resources'):
        for filename in os.listdir('resources'):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg')):
                shutil.copy2(os.path.join('resources', filename), os.path.join('output/images', filename))

def generate_archive_content(posts):
    content = ""
    current_year = None
    for post in posts:
        year = post['date'].year
        if year != current_year:
            if current_year is not None:
                content += "</ul>"
            content += f"<h2>{year}</h2><ul>"
            current_year = year
        content += f"""<li>
            <span>{post['date'].strftime('%B %d')}</span> -
            <a href='{post['url']}'>{post['title']}</a>
            <div class="tags">
                {' '.join(f'<a href="/tags/{tag.lower().replace(" ", "-")}.html" class="tag">{tag}</a>' for tag in post['tags'])}
            </div>
        </li>"""
    content += "</ul>"
    return content

def generate_tags_content(tags):
    content = "<h2>Tags</h2><ul>"
    for tag, posts in sorted(tags.items()):
        content += f"<li><a href='/tags/{tag.lower().replace(' ', '-')}.html'>{tag}</a> ({len(posts)})</li>"
    content += "</ul>"
    return content

def generate_rss(posts, site_config):
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = site_config['site_title']
    ET.SubElement(channel, "description").text = site_config['site_subtitle']
    ET.SubElement(channel, "link").text = site_config['site_url']
    ET.SubElement(channel, "lastBuildDate").text = formatdate(localtime=True)

    for post in posts[:10]:  # Include only the 10 most recent posts
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = post['title']
        ET.SubElement(item, "link").text = f"{site_config['site_url']}{post['url']}"
        ET.SubElement(item, "description").text = post['content'][:200] + "..."  # First 200 characters as description
        ET.SubElement(item, "pubDate").text = formatdate(post['date'].timestamp(), localtime=True)
        ET.SubElement(item, "guid").text = f"{site_config['site_url']}{post['url']}"

    tree = ET.ElementTree(rss)
    tree.write("output/rss.xml", encoding="UTF-8", xml_declaration=True)

def generate_site():
    # Get site configuration
    site_config = get_site_config()

    # Create output directories
    ensure_directory('output')
    ensure_directory('output/posts')
    ensure_directory('output/tags')

    # Copy images from resources to output/images
    copy_images()

    # Get all markdown files from posts directory
    posts = []
    tags = defaultdict(list)
    for filename in os.listdir('posts'):
        if filename.endswith('.md'):
            file_path = os.path.join('posts', filename)
            html, meta = parse_markdown(file_path)
            post_tags = parse_tags(meta.get('tags', [''])[0])
            post = {
                'content': html,
                'title': meta.get('title', [''])[0],
                'date': datetime.strptime(meta.get('date', [''])[0], '%Y-%m-%d'),
                'tags': post_tags,
                'url': f"/posts/{meta.get('title', [''])[0].lower().replace(' ', '-')}.html",
                'read_time': len(html.split()) // 200 + 1,
                'is_post': True
            }
            posts.append(post)
            for tag in post_tags:
                tags[tag].append(post)

    # Sort posts by date
    posts.sort(key=lambda x: x['date'], reverse=True)

    # Render index page
    index_template = env.get_template('index.html')
    output = index_template.render(
        posts=posts[:10],  # Only display the 10 most recent posts
        page_title="Recent Posts",
        total_posts=len(posts),
        **site_config
    )
    with open('output/index.html', 'w') as f:
        f.write(output)

    # Render individual post pages
    post_template = env.get_template('post.html')
    for post in posts:
        output = post_template.render(post=post, page_title=post['title'], **site_config)
        with open(f"output{post['url']}", 'w') as f:
            f.write(output)

    # Render archive page
    archive_content = generate_archive_content(posts)
    archive_post = {
        'content': archive_content,
        'title': 'Archive',
        'tags': [],
        'url': '/archive.html',
        'is_post': False
    }
    output = post_template.render(post=archive_post, page_title="Archive", **site_config)
    with open('output/archive.html', 'w') as f:
        f.write(output)

    # Render tags page
    tags_content = generate_tags_content(tags)
    tags_post = {
        'content': tags_content,
        'title': 'Tags',
        'tags': [],
        'url': '/tags.html',
        'is_post': False
    }
    output = post_template.render(post=tags_post, page_title="Tags", **site_config)
    with open('output/tags.html', 'w') as f:
        f.write(output)

    # Render individual tag pages
    tag_template = env.get_template('tag.html')
    for tag, tag_posts in tags.items():
        output = tag_template.render(tag=tag, posts=tag_posts, page_title=f'Posts Tagged "{tag}"', **site_config)
        with open(f"output/tags/{tag.lower().replace(' ', '-')}.html", 'w') as f:
            f.write(output)

    # Render pages from 'pages' directory
    for filename in os.listdir('pages'):
        if filename.endswith('.md'):
            file_path = os.path.join('pages', filename)
            html, meta = parse_markdown(file_path)
            page = {
                'content': html,
                'title': meta.get('title', [''])[0],
                'tags': meta.get('tags', []),
                'url': f"/{filename.replace('.md', '.html')}",
                'is_post': False
            }
            output = post_template.render(post=page, page_title=page['title'], **site_config)
            with open(f"output{page['url']}", 'w') as f:
                f.write(output)

    # Generate RSS feed
    generate_rss(posts, site_config)

if __name__ == '__main__':
    generate_site()
