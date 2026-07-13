from __future__ import annotations

import re
from xml.sax.saxutils import escape


def build_blogger_xml(structure: dict, *, template_name: str = "simple") -> str:
    """
    Build a minimal but importable Blogger theme XML.

    Uses classic Blogger layout with header, main (Blog), optional sidebar, footer.
    """
    title = escape(str(structure.get("title") or "My Blog"))
    colors = structure.get("colors") or {}
    fonts = structure.get("fonts") or {}
    primary = escape(str(colors.get("primary") or "#1a73e8"))
    secondary = escape(str(colors.get("secondary") or "#34a853"))
    background = escape(str(colors.get("background") or "#ffffff"))
    text = escape(str(colors.get("text") or "#222222"))
    body_font = escape(str(fonts.get("body") or "system-ui, sans-serif"))
    heading_font = escape(str(fonts.get("heading") or body_font))
    layout = str(structure.get("layout") or "single-column")
    features = structure.get("features") or {}
    has_sidebar = bool(features.get("sidebar")) or layout == "two-column"
    dense = bool(features.get("dense"))
    post_pad = "0.6rem 0.85rem" if dense else "1rem 1.25rem"
    content_pad = "0.5rem" if dense else "1rem"

    nav = structure.get("nav_links") or []
    nav_html = "".join(
        f'<li><a expr:href="data:blog.homepageUrl">{escape(str(n.get("label") or "Link"))}</a></li>'
        for n in nav[:8]
    )
    if not nav_html:
        nav_html = (
            '<li><a expr:href="data:blog.homepageUrl">Home</a></li>'
            '<li><a href="#">About</a></li>'
        )

    description = escape(str(structure.get("description") or "Powered by BloggerEasy"))

    skin_css = f"""
body {{
  margin: 0;
  font-family: {body_font};
  color: {text};
  background: {background};
  line-height: 1.6;
}}
a {{ color: {primary}; }}
.header-inner {{
  background: {primary};
  color: #fff;
  padding: 1.5rem 1rem;
}}
.header-inner h1, .header-inner a {{ color: #fff; text-decoration: none; font-family: {heading_font}; }}
.nav-bar {{
  background: {secondary};
  padding: 0.5rem 1rem;
}}
.nav-bar ul {{ list-style: none; margin: 0; padding: 0; display: flex; gap: 1rem; flex-wrap: wrap; }}
.nav-bar a {{ color: #fff; text-decoration: none; }}
.content-wrap {{
  max-width: 1100px;
  margin: 0 auto;
  padding: {content_pad};
  display: grid;
  grid-template-columns: {"1fr 300px" if has_sidebar else "1fr"};
  gap: {"1rem" if dense else "1.5rem"};
}}
.post {{
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: {post_pad};
  margin-bottom: {"0.6rem" if dense else "1rem"};
}}
.post h3 {{ font-family: {heading_font}; margin-top: 0; }}
.sidebar .widget {{
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
}}
.footer-inner {{
  margin-top: 2rem;
  padding: 1rem;
  text-align: center;
  background: #0f172a;
  color: #e2e8f0;
  font-size: 0.9rem;
}}
@media (max-width: 800px) {{
  .content-wrap {{ grid-template-columns: 1fr; }}
}}
""".strip()

    sidebar_section = ""
    if has_sidebar:
        sidebar_section = """
  <div class='column-right-outer'>
    <div class='column-right-inner'>
      <aside>
      <b:section class='sidebar' id='sidebar' name='Sidebar' showaddelement='yes'>
        <b:widget id='Profile1' locked='false' title='About Me' type='Profile' version='1'>
          <b:widget-settings>
            <b:widget-setting name='showaboutme'>true</b:widget-setting>
            <b:widget-setting name='showlocation'>false</b:widget-setting>
          </b:widget-settings>
          <b:includable id='main'><div class='widget-content'><data:title/></div></b:includable>
        </b:widget>
        <b:widget id='Label1' locked='false' title='Labels' type='Label' version='1'>
          <b:includable id='main'><div class='widget-content'><data:title/></div></b:includable>
        </b:widget>
      </b:section>
      </aside>
    </div>
  </div>
"""

    # Blogger expects a full XML document with b: namespace
    xml = f"""<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE html>
<html b:css='false' b:defaultwidgetversion='2' b:layoutsVersion='3' b:responsive='true'
  b:templateVersion='1.0.0' expr:class='data:blog.languageDirection'
  xmlns='http://www.w3.org/1999/xhtml'
  xmlns:b='http://www.google.com/2005/gml/b'
  xmlns:data='http://www.google.com/2005/gml/data'
  xmlns:expr='http://www.google.com/2005/gml/expr'>
<head>
  <meta charset='utf-8'/>
  <meta content='width=device-width, initial-scale=1' name='viewport'/>
  <title><data:blog.pageTitle/></title>
  <b:include data='blog' name='all-head-content'/>
  <b:skin version='1.0.0'><![CDATA[
/*-----------------------------------------------
BloggerEasy generated theme
Template: {escape(template_name)}
-----------------------------------------------*/
{skin_css}
]]></b:skin>
</head>
<body>
  <div class='header-outer'>
    <header class='header-inner'>
      <b:section class='header' id='header' maxwidgets='1' name='Header' showaddelement='no'>
        <b:widget id='Header1' locked='true' title='{title}' type='Header' version='1'>
          <b:widget-settings>
            <b:widget-setting name='displayUrl'/>
            <b:widget-setting name='displayHeight'>0</b:widget-setting>
            <b:widget-setting name='sectionWidth'>-1</b:widget-setting>
            <b:widget-setting name='useImage'>false</b:widget-setting>
            <b:widget-setting name='shrinkToFit'>false</b:widget-setting>
            <b:widget-setting name='imagePlacement'>BEHIND</b:widget-setting>
            <b:widget-setting name='displayWidth'>-1</b:widget-setting>
          </b:widget-settings>
          <b:includable id='main'>
            <div id='header-inner'>
              <h1><b:include name='title'/></h1>
              <p><data:blog.metaDescription/></p>
            </div>
          </b:includable>
        </b:widget>
      </b:section>
    </header>
    <nav class='nav-bar'>
      <ul>
        {nav_html}
      </ul>
    </nav>
  </div>

  <div class='content-wrap'>
    <div class='main-outer'>
      <b:section class='main' id='main' name='Main' showaddelement='yes'>
        <b:widget id='Blog1' locked='true' title='Blog Posts' type='Blog' version='1'>
          <b:includable id='main'>
            <b:loop values='data:posts' var='post'>
              <article class='post'>
                <h3><a expr:href='data:post.url'><data:post.title/></a></h3>
                <div class='post-body'><data:post.body/></div>
              </article>
            </b:loop>
          </b:includable>
        </b:widget>
      </b:section>
    </div>
    {sidebar_section}
  </div>

  <footer class='footer-inner'>
    <b:section class='footer' id='footer' name='Footer' showaddelement='yes'>
      <b:widget id='Text1' locked='false' title='Footer' type='Text' version='1'>
        <b:widget-settings>
          <b:widget-setting name='content'>{description} · Theme by BloggerEasy</b:widget-setting>
        </b:widget-settings>
        <b:includable id='main'><div class='widget-content'><data:content/></div></b:includable>
      </b:widget>
    </b:section>
  </footer>
</body>
</html>
"""
    return xml


def sanitize_filename(name: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", name.strip()).strip("-").lower()
    return slug or "theme"
