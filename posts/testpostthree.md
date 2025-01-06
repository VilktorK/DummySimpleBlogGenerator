---
title: My Third Blog Post
date: 2024-11-20
tags: [sharks, blogging, cats, python]
---

# Welcome to My Third Blog Post

This is my first blog post using a static site generator.

<!-- ![Dog Image](resources/image.JPG) -->
<!-- Image Credits: LuKaS Cuba -->
<!-- images don't yet fit to the page but this is how to add them -->

## List
1. Item One
2. Item Two
3. Item Three

Code Example
<pre><code>
python
get_venv_python_version() {
    local venv_path="$1"
    local version=""
    
    if [ -f "$venv_path/.python-version" ]; then
        version=$(cat "$venv_path/.python-version")
    elif [ -f "$venv_path/bin/python" ]; then
        version=$("$venv_path/bin/python" --version 2>&1)
    else
        version="Unknown"
    fi
    
    echo "$version"
}
</code></pre>

[Dummy-Simple-Distrobox-Manager]: https://github.com/VilktorK/DummySimpleDistroboxManager

[Dummy Simple Venv Manager](https://github.com/VilktorK/DummySimpleVenvManager)

[Dummy Simple Distrobox Manager][Dummy-Simple-Distrobox-Manager]
