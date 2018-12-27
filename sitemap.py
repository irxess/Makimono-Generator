import glob

def create_xml_url_from_glob(name, modified=""):
    url_xml = \
f"""
  <url>
    <loc>https://www.makimo.no/{name}</loc>
"""
    if modified != "":
        url_xml += f"    <lastmod>{modified}</lastmod>\n"
    url_xml += "  </url>"
    return url_xml

def create_sitemap(recipes):
    sitemap = \
"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">"""
    # Go through files in root folder
    for filename in glob.iglob('publish/*.html', recursive=True):
        sitemap += create_xml_url_from_glob(filename[8:])

    # Go through files in the all folder
    for filename in glob.iglob('publish/all/*.html', recursive=True):
        sitemap += create_xml_url_from_glob(filename[8:])

    for recipe in recipes:
        sitemap += create_xml_url_from_glob(recipe.url, recipe.updated)

    sitemap += "\n</urlset>"

    return(sitemap)

