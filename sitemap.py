import glob

xmlIndent = '  '

def fix_path_when_broken_by_windows(path):
    path = path.replace("\\", "/")
    return path

def create_xml_url_from_glob(name, modified=""):
    url_xml = \
f"""
{xmlIndent}<url>
{2*xmlIndent}<loc>https://www.makimo.no/{name}</loc>
"""
    if modified != "":
        url_xml += f"{2*xmlIndent}<lastmod>{modified}</lastmod>\n"
    url_xml += f"{xmlIndent}</url>"
    return url_xml

def create_sitemap(recipes):
    sitemap = \
"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">"""
    # Go through files in root folder
    for filename in glob.iglob('publish/*.html', recursive=True):
        path_from_web_base = filename[8:]
        safe_path = fix_path_when_broken_by_windows(path_from_web_base)
        sitemap += create_xml_url_from_glob(safe_path)

    # Go through files in the all folder
    for filename in glob.iglob('publish/all/*.html', recursive=True):
        path_from_web_base = filename[8:]
        safe_path = fix_path_when_broken_by_windows(path_from_web_base)
        sitemap += create_xml_url_from_glob(safe_path)

    for recipe in recipes:
        sitemap += create_xml_url_from_glob(recipe.url, recipe.updated)

    sitemap += "\n</urlset>"

    return(sitemap)

