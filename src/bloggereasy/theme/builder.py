from __future__ import annotations

import re
from xml.sax.saxutils import escape

from bloggereasy.theme.models import PageStructure, structure_dict


def build_blogger_xml(structure: PageStructure | dict, *, template_name: str = "simple") -> str:
    """
    Build a minimal but importable Blogger theme XML.

    Uses classic Blogger layout with header, main (Blog), optional sidebar, footer.
    """
    structure = structure_dict(structure)
    title = escape(str(structure.get("title") or "My Blog"))
    colors = structure.get("colors") or {}
    fonts = structure.get("fonts") or {}
    primary = escape(str(colors.get("primary") or "#1a73e8"))
    secondary = escape(str(colors.get("secondary") or "#34a853"))
    background = escape(str(colors.get("background") or "#ffffff"))
    text = escape(str(colors.get("text") or "#222222"))
    surface = escape(str(colors.get("surface") or "#ffffff"))
    muted = escape(str(colors.get("muted") or "#f8fafc"))
    border = escape(str(colors.get("border") or "#e5e7eb"))
    footer = escape(str(colors.get("footer") or "#0f172a"))
    footer_text = escape(str(colors.get("footer_text") or "#e2e8f0"))
    body_font = escape(str(fonts.get("body") or "system-ui, sans-serif"))
    heading_font = escape(str(fonts.get("heading") or body_font))
    skin = structure.get("skin") or {}
    spacing = skin.get("spacing") or {}
    buttons = skin.get("buttons") or {}
    layout = str(structure.get("layout") or "single-column")
    features = structure.get("features") or {}
    has_sidebar = bool(features.get("sidebar")) or layout in {"two-column", "three-column"}
    has_left_rail = bool(features.get("magazine_left_rail")) or layout == "three-column"
    widget_mode = str(features.get("widgets") or "default")
    dense = bool(features.get("dense"))
    post_pad = "0.6rem 0.85rem" if dense else str(spacing.get("card_padding") or "1rem 1.25rem")
    content_pad = "0.5rem" if dense else str(spacing.get("section_padding") or "1rem")
    gap = "1rem" if dense else str(spacing.get("gap") or "1.5rem")
    radius = str(spacing.get("radius") or "8px")
    button_bg = escape(str(buttons.get("background") or primary))
    button_text = escape(str(buttons.get("color") or "#ffffff"))
    button_pad = escape(str(buttons.get("padding") or "0.55rem 0.9rem"))
    button_radius = escape(str(buttons.get("radius") or "6px"))

    nav = structure.get("nav_links") or []
    nav_html = "".join(
        f'<li><a expr:href="data:blog.homepageUrl">{escape(str(n.get("label") or "Link"))}</a></li>'
        for n in nav[:8]
    )
    if not nav_html:
        nav_html = (
            '<li><a expr:href="data:blog.homepageUrl">Home</a></li><li><a href="#">About</a></li>'
        )
    nav_widget = _nav_linklist_widget(nav)

    description = escape(str(structure.get("description") or "Powered by BloggerEasy"))

    skin_css = f"""
body {{
  margin: 0;
  font-family: {body_font};
  color: {text};
  background: {background};
  line-height: 1.6;
  overflow-wrap: anywhere;
}}
a {{ color: {primary}; }}
img, iframe, video {{
  max-width: 100%;
  height: auto;
}}
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
  grid-template-columns: {"220px 1fr 260px" if has_left_rail else "1fr 300px" if has_sidebar else "1fr"};
  gap: {gap};
}}
.magazine-featured {{
  background: #fff7ed;
  border: 1px solid #fed7aa;
  border-radius: 8px;
  padding: 0.75rem;
}}
.post {{
  background: {surface};
  border: 1px solid {border};
  border-radius: {radius};
  padding: {post_pad};
  margin-bottom: {"0.6rem" if dense else "1rem"};
}}
.post h3 {{ font-family: {heading_font}; margin-top: 0; }}
.post a, .button, button {{
  background: {button_bg};
  color: {button_text};
  padding: {button_pad};
  border-radius: {button_radius};
}}
.sidebar .widget {{
  background: {muted};
  border: 1px solid {border};
  border-radius: {radius};
  padding: 1rem;
  margin-bottom: 1rem;
}}
.footer-inner {{
  margin-top: 2rem;
  padding: 1rem;
  text-align: center;
  background: {footer};
  color: {footer_text};
  font-size: 0.9rem;
}}
@media (max-width: 800px) {{
  .content-wrap {{ grid-template-columns: 1fr; }}
  .header-inner {{ padding: 1rem; }}
  .header-inner h1 {{ font-size: 1.65rem; line-height: 1.2; }}
  .nav-bar ul {{ gap: 0.45rem; }}
  .nav-bar a {{ display: inline-block; padding: 0.25rem 0; }}
  .post {{ padding: 0.85rem; }}
  .sidebar .widget {{ padding: 0.85rem; }}
}}
@media (max-width: 480px) {{
  .content-wrap {{ padding: 0.5rem; }}
  .nav-bar {{ padding: 0.45rem 0.65rem; }}
  .nav-bar ul {{ flex-direction: column; gap: 0.25rem; }}
  .footer-inner {{ font-size: 0.82rem; }}
}}
""".strip()

    sidebar_section = ""
    if has_sidebar:
        sidebar_widgets = _sidebar_widgets(widget_mode)
        sidebar_section = f"""
  <div class='column-right-outer'>
    <div class='column-right-inner'>
      <aside>
      <b:section class='sidebar' id='sidebar' name='Sidebar' showaddelement='yes'>
        {sidebar_widgets}
      </b:section>
</aside>
    </div>
  </div>
"""

    left_rail_section = ""
    if has_left_rail:
        left_rail_section = """
    <div class='column-left-outer'>
      <div class='column-left-inner'>
        <aside class='magazine-featured'>
        <b:section class='magazine-left' id='magazine-left' name='Magazine Left Rail' showaddelement='yes'>
          <b:widget id='TextFeatured1' locked='false' title='Featured' type='Text' version='1'>
            <b:widget-settings>
              <b:widget-setting name='content'>Featured story and editor picks</b:widget-setting>
            </b:widget-settings>
            <b:includable id='main'><div class='widget-content'><data:content/></div></b:includable>
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
  <meta expr:content='data:blog.metaDescription' name='description'/>
  <meta expr:content='data:blog.title' property='og:site_name'/>
  <meta expr:content='data:blog.pageTitle' property='og:title'/>
  <meta expr:content='data:blog.metaDescription' property='og:description'/>
  <meta expr:content='data:blog.canonicalUrl' property='og:url'/>
  <meta content='website' property='og:type'/>
  <meta content='summary_large_image' name='twitter:card'/>
  <meta expr:content='data:blog.pageTitle' name='twitter:title'/>
  <meta expr:content='data:blog.metaDescription' name='twitter:description'/>
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
      {nav_widget}
    </nav>
  </div>

  <div class='content-wrap'>
    {left_rail_section}
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


def _nav_linklist_widget(nav: list[dict]) -> str:
    links = nav[:8] or [{"label": "Home", "href": "#"}, {"label": "About", "href": "#"}]
    settings = ["<b:widget-setting name='sorting'>NONE</b:widget-setting>"]
    for i, item in enumerate(links):
        label = escape(str(item.get("label") or "Link"))
        href = escape(str(item.get("href") or "#"))
        settings.append(f"<b:widget-setting name='link-{i}'>{href}</b:widget-setting>")
        settings.append(f"<b:widget-setting name='link-{i}.name'>{label}</b:widget-setting>")
    settings_xml = "\n            ".join(settings)
    return f"""
      <b:section class='nav-widgets' id='navigation' name='Navigation' showaddelement='yes'>
        <b:widget id='LinkList1' locked='false' title='Navigation' type='LinkList' version='1'>
          <b:widget-settings>
            {settings_xml}
          </b:widget-settings>
          <b:includable id='main'><div class='widget-content'><data:title/></div></b:includable>
        </b:widget>
      </b:section>"""


def _sidebar_widgets(mode: str) -> str:
    profile = """
        <b:widget id='Profile1' locked='false' title='About Me' type='Profile' version='1'>
          <b:widget-settings>
            <b:widget-setting name='showaboutme'>true</b:widget-setting>
            <b:widget-setting name='showlocation'>false</b:widget-setting>
          </b:widget-settings>
          <b:includable id='main'><div class='widget-content'><data:title/></div></b:includable>
        </b:widget>"""
    labels = """
        <b:widget id='Label1' locked='false' title='Labels' type='Label' version='1'>
          <b:includable id='main'><div class='widget-content'><data:title/></div></b:includable>
        </b:widget>"""
    popular = """
        <b:widget id='PopularPosts1' locked='false' title='Popular Posts' type='PopularPosts' version='1'>
          <b:includable id='main'><div class='widget-content'><data:title/></div></b:includable>
        </b:widget>"""
    archive = """
        <b:widget id='BlogArchive1' locked='false' title='Archive' type='BlogArchive' version='1'>
          <b:includable id='main'><div class='widget-content'><data:title/></div></b:includable>
        </b:widget>"""
    if mode == "minimal":
        return profile
    if mode == "full":
        return popular + labels + archive + profile
    return profile + labels
