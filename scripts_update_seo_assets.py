from pathlib import Path
from bs4 import BeautifulSoup
from xml.etree import ElementTree as ET

ROOT = Path('/home/ubuntu/bestbuilderuk')
BLOG_DIR = ROOT / 'blog'
SITE = 'https://ab-construction-swadlincote.surge.sh'
DATE = '2026-04-12'

LANDING_PAGES = [
    ('House Extensions Swadlincote', 'extensions-swadlincote.html', 'Rear, side and two-storey extension advice for homeowners in Swadlincote and South Derbyshire.'),
    ('Loft Conversions Swadlincote & South Derbyshire', 'loft-conversions-swadlincote.html', 'A local landing page for loft conversion projects across Swadlincote, Burton upon Trent, and nearby areas.'),
    ('Kitchen Fitter Burton upon Trent', 'kitchen-fitter-burton.html', 'Kitchen fitting, renovation, and layout advice for homeowners in Burton upon Trent.'),
    ('Bathroom Fitter Swadlincote', 'bathroom-fitter-swadlincote.html', 'Bathroom fitting and refurbishment support for homes across Swadlincote.'),
    ('Home Renovation Swadlincote', 'renovation-swadlincote.html', 'A renovation landing page focused on layout upgrades, refurbishment, and whole-home improvements.'),
    ('Garage Conversions Swadlincote', 'garage-conversions-swadlincote.html', 'Garage conversion ideas for Swadlincote households looking to add usable living space.'),
    ('Builder Near Me Derbyshire', 'builder-near-me-derbyshire.html', 'A location-led service page for homeowners searching for a reliable local builder in Derbyshire.')
]

FEATURED_ARTICLES = [
    'cost-of-building-an-extension-in-south-derbyshire-2026.html',
    'do-you-need-planning-permission-for-an-extension-in-swadlincote.html',
    'how-to-choose-a-reliable-builder-in-swadlincote.html',
    'two-storey-extension-in-woodville-adding-space-for-a-growing-family.html',
    'loft-conversion-in-burton-upon-trent-from-unused-attic-to-master-bedroom.html',
    'kitchen-renovation-in-newhall-complete-transformation.html',
    'full-bathroom-refit-in-swadlincote-modern-design-on-a-budget.html',
]


def parse_article(path: Path):
    soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
    title = soup.title.get_text(strip=True).replace(' | AB Construction UK Ltd', '') if soup.title else path.stem.replace('-', ' ').title()
    desc = ''
    meta = soup.find('meta', attrs={'name': 'description'})
    if meta and meta.get('content'):
        desc = meta['content']
    desc = desc or 'Expert building advice from AB Construction UK Ltd for homeowners in Swadlincote and South Derbyshire.'
    published = 'April 2026'
    icon = '🏡'
    lower = (title + ' ' + desc).lower()
    if 'cost' in lower or 'budget' in lower:
        icon = '💷'
    elif 'planning' in lower or 'permission' in lower:
        icon = '📋'
    elif 'builder' in lower:
        icon = '🔨'
    elif 'bathroom' in lower:
        icon = '🛁'
    elif 'kitchen' in lower:
        icon = '🍳'
    elif 'loft' in lower:
        icon = '🏠'
    elif 'extension' in lower:
        icon = '🏗️'
    elif 'renovation' in lower:
        icon = '🧰'
    return {
        'slug': path.name,
        'title': title,
        'description': desc,
        'published': published,
        'icon': icon,
    }


def ordered_articles():
    all_articles = {p.name: parse_article(p) for p in BLOG_DIR.glob('*.html')}
    ordered = []
    for slug in FEATURED_ARTICLES:
        if slug in all_articles:
            ordered.append(all_articles.pop(slug))
    for slug in sorted(all_articles):
        ordered.append(all_articles[slug])
    return ordered


def build_blog_html():
    cards = []
    for article in ordered_articles():
        cards.append(f'''<div class="service-card fade-in">
<div class="service-card-icon" style="height:120px; font-size:2rem; background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%); color: white; display: flex; align-items: center; justify-content: center; border-radius: var(--radius) var(--radius) 0 0;">{article['icon']}</div>
<div class="service-card-body">
<h3><a href="blog/{article['slug']}" style="color:var(--primary);">{article['title']}</a></h3>
<p style="font-size:0.85rem; color:var(--gray-500); margin-bottom:8px;">Published {article['published']}</p>
<p>{article['description']}</p>
<a class="btn btn-primary btn-sm" href="blog/{article['slug']}" style="margin-top:10px;">Read Article</a>
</div>
</div>''')

    landing_links = '\n'.join(
        f'<li><a href="{href}">{title}</a> — {summary}</li>'
        for title, href, summary in LANDING_PAGES
    )

    featured_links = '\n'.join(
        f'<li><a href="blog/{slug}">{parse_article(BLOG_DIR / slug)["title"]}</a></li>'
        for slug in FEATURED_ARTICLES if (BLOG_DIR / slug).exists()
    )

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Construction Blog | Expert Building Advice | AB Construction UK Ltd Swadlincote</title>
<meta content="The official blog of AB Construction UK Ltd. Expert tips, advice, and insights on home extensions, loft conversions, kitchen renovations, and building projects in Swadlincote and South Derbyshire." name="description"/>
<meta content="construction blog, building advice Swadlincote, home improvement tips South Derbyshire, builders blog, AB Construction blog" name="keywords"/>
<meta content="AB Construction UK Ltd" name="author"/>
<meta content="index, follow" name="robots"/>
<meta content="Construction Blog | AB Construction UK Ltd" property="og:title"/>
<meta content="Expert tips, advice, and insights on home extensions, loft conversions, kitchen renovations, and building projects in Swadlincote." property="og:description"/>
<meta content="website" property="og:type"/>
<meta content="{SITE}/blog.html" property="og:url"/>
<meta content="{SITE}/images/hero-bg.jpg" property="og:image"/>
<meta content="AB Construction UK Ltd" property="og:site_name"/>
<meta content="summary_large_image" name="twitter:card"/>
<meta content="Construction Blog | AB Construction UK Ltd" name="twitter:title"/>
<meta content="Expert tips and advice for your next home improvement project in South Derbyshire." name="twitter:description"/>
<meta content="{SITE}/images/hero-bg.jpg" name="twitter:image"/>
<link href="{SITE}/blog.html" rel="canonical"/>
<link href="css/style.css" rel="stylesheet"/>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "AB Construction UK Ltd Blog",
  "url": "{SITE}/blog.html",
  "description": "Construction advice, local guides, and project case studies from AB Construction UK Ltd."
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "{SITE}/#localbusiness",
  "name": "AB Construction UK Ltd",
  "url": "{SITE}",
  "telephone": ["+441283310115", "+447710280062"],
  "email": "adamsessions39@gmail.com",
  "address": {{
    "@type": "PostalAddress",
    "addressLocality": "Swadlincote",
    "addressRegion": "Derbyshire",
    "addressCountry": "GB"
  }},
  "areaServed": ["Swadlincote", "South Derbyshire", "Derbyshire", "Burton upon Trent", "Derby", "Ashby-de-la-Zouch", "Midlands"],
  "description": "Brickwork, joinery, extensions, loft conversions, kitchens, bathrooms, and renovation works across Swadlincote and the wider Derbyshire area."
}}
</script>
</head>
<body>
<!-- Last automated refresh: 2026-04-12 14:20:00 UTC -->
<div class="top-bar">
<div class="container">
<div class="top-bar-left">
<span>📍 Swadlincote, Derbyshire, UK</span>
<span>⏰ Mon-Fri: 7am-6pm | Sat: 8am-2pm</span>
</div>
<div class="top-bar-right">
<a class="phone-link" href="tel:01283310115">📞 01283 310115</a>
<a class="phone-link" href="tel:07710280062">📱 07710 280062</a>
</div>
</div>
</div>
<header class="header">
<div class="container">
<a class="logo" href="index.html">
<div class="logo-text">
<div class="company-name"><span>AB</span> CONSTRUCTION</div>
<div class="company-sub">LTD • Building Dreams, Delivering Quality</div>
</div>
</a>
<button aria-label="Toggle menu" class="menu-toggle">
<span></span><span></span><span></span>
</button>
<nav class="nav">
<ul class="nav-list">
<li><a href="referral.html">Refer a Friend</a></li>
<li><a href="index.html">Home</a></li>
<li>
<a href="#">Services ▾</a>
<div class="dropdown">
<a href="services/brickwork.html">Brickwork</a>
<a href="services/joinery.html">Joinery</a>
<a href="services/extensions.html">Extensions</a>
<a href="services/loft-conversions.html">Loft Conversions</a>
<a href="services/kitchens.html">Kitchens</a>
<a href="services/bathrooms.html">Bathrooms</a>
<a href="services/renovation-works.html">Renovation Works</a>
</div>
</li>
<li><a href="portfolio.html">Portfolio</a></li>
<li><a class="active" href="blog.html">Blog</a></li>
<li><a href="faq.html">FAQ</a></li>
<li><a href="index.html#about">About Us</a></li>
<li><a href="index.html#contact">Contact</a></li>
</ul>
</nav>
</div>
</header>
<section class="page-hero">
<div class="page-hero-content">
<h1>Construction &amp; Building Blog</h1>
<p>Expert tips, cost guides, local case studies, and practical building advice for homeowners in Swadlincote and South Derbyshire.</p>
<div class="breadcrumb">
<a href="index.html">Home</a> <span>/</span> Blog
</div>
</div>
</section>
<section class="section">
<div class="container">
<div class="section-title fade-in">
<h2>Local Project Guides &amp; Service Pages</h2>
<div class="accent-line"></div>
<p>Use these location-specific landing pages and local homeowner guides to compare options, understand costs, and explore related services across South Derbyshire.</p>
</div>
<div class="feature-item fade-in" style="max-width:none; background:#fff; padding:30px; border-radius:var(--radius); box-shadow:var(--shadow-md);">
<ul>
{landing_links}
</ul>
<p><strong>Featured local guides:</strong></p>
<ul>
{featured_links}
</ul>
</div>
</div>
</section>
<section class="section">
<div class="container">
<div class="section-title fade-in">
<h2>Latest Articles</h2>
<div class="accent-line"></div>
<p>Helpful guides and insights from the AB Construction team to help you plan your next project.</p>
</div>
<div class="services-grid">
{''.join(cards)}
</div>
</div>
</section>
<section class="cta-section">
<div class="container">
<h2>Ready to Start Your Project?</h2>
<p>Call us today for a free, no-obligation quote. We are here to help bring your vision to life.</p>
<div class="hero-buttons">
<a class="btn btn-primary" href="tel:01283310115">📞 Call 01283 310115</a>
<a class="btn btn-outline" href="tel:07710280062">📱 Call 07710 280062</a>
</div>
</div>
</section>
<footer class="footer">
<div class="container">
<div class="footer-grid">
<div class="footer-col">
<h4>AB Construction UK Ltd</h4>
<p>Building Dreams, Delivering Quality. We are Swadlincote's trusted construction company, delivering expert building services with pride and professionalism.</p>
<p>From small repairs to large-scale renovations, no project is too big or too small for our experienced team.</p>
</div>
<div class="footer-col">
<h4>Our Services</h4>
<ul>
<li><a href="services/brickwork.html">Brickwork</a></li>
<li><a href="services/joinery.html">Joinery</a></li>
<li><a href="services/extensions.html">Extensions</a></li>
<li><a href="services/loft-conversions.html">Loft Conversions</a></li>
<li><a href="services/kitchens.html">Kitchens</a></li>
<li><a href="services/bathrooms.html">Bathrooms</a></li>
<li><a href="services/renovation-works.html">Renovation Works</a></li>
</ul>
</div>
<div class="footer-col">
<h4>Quick Links</h4>
<ul>
<li><a href="index.html">Home</a></li>
<li><a href="portfolio.html">Portfolio</a></li>
<li><a href="blog.html">Blog</a></li>
<li><a href="faq.html">FAQ</a></li>
<li><a href="index.html#about">About Us</a></li>
<li><a href="index.html#contact">Contact Us</a></li>
</ul>
</div>
<div class="footer-col">
<h4>Contact Us</h4>
<p>Swadlincote, Derbyshire, UK</p>
<p><a href="tel:01283310115">01283 310115</a><br/><a href="tel:07710280062">07710 280062</a></p>
<p><a href="mailto:adamsessions39@gmail.com">adamsessions39@gmail.com</a></p>
</div>
</div>
<div class="footer-bottom"><p>© 2026 AB Construction UK Ltd. All rights reserved.</p></div>
</div>
</footer>
<script src="js/main.js"></script>
</body>
</html>
'''
    (ROOT / 'blog.html').write_text(html, encoding='utf-8')


def update_homepage():
    path = ROOT / 'index.html'
    text = path.read_text(encoding='utf-8')
    block = '''</section>
<section class="section">
<div class="container">
<div class="section-title fade-in">
<h2>Local Service Pages & Planning Guides</h2>
<div class="accent-line"></div>
<p>Explore our new location-specific landing pages and practical homeowner guides covering extensions, loft conversions, kitchens, bathrooms, renovations, and choosing a reliable builder in South Derbyshire.</p>
</div>
<div class="services-grid">
<div class="service-card fade-in"><div class="service-card-body"><h3><a href="extensions-swadlincote.html" style="color:var(--primary);">House Extensions Swadlincote</a></h3><p>Local extension advice, FAQs, and next steps for homeowners planning more space.</p></div></div>
<div class="service-card fade-in"><div class="service-card-body"><h3><a href="loft-conversions-swadlincote.html" style="color:var(--primary);">Loft Conversions Swadlincote & South Derbyshire</a></h3><p>Learn how a loft conversion can create extra living space without moving home.</p></div></div>
<div class="service-card fade-in"><div class="service-card-body"><h3><a href="kitchen-fitter-burton.html" style="color:var(--primary);">Kitchen Fitter Burton upon Trent</a></h3><p>Find kitchen fitting and renovation advice for Burton upon Trent households.</p></div></div>
<div class="service-card fade-in"><div class="service-card-body"><h3><a href="bathroom-fitter-swadlincote.html" style="color:var(--primary);">Bathroom Fitter Swadlincote</a></h3><p>Explore bathroom fitting, modernisation, and budget planning advice.</p></div></div>
<div class="service-card fade-in"><div class="service-card-body"><h3><a href="renovation-swadlincote.html" style="color:var(--primary);">Home Renovation Swadlincote</a></h3><p>Planning a full refurbishment? See what to consider before work starts.</p></div></div>
<div class="service-card fade-in"><div class="service-card-body"><h3><a href="garage-conversions-swadlincote.html" style="color:var(--primary);">Garage Conversions Swadlincote</a></h3><p>Convert underused garage space into an office, playroom, or extra lounge.</p></div></div>
<div class="service-card fade-in"><div class="service-card-body"><h3><a href="builder-near-me-derbyshire.html" style="color:var(--primary);">Builder Near Me Derbyshire</a></h3><p>Compare what to look for when hiring a dependable local builder.</p></div></div>
<div class="service-card fade-in"><div class="service-card-body"><h3><a href="blog/cost-of-building-an-extension-in-south-derbyshire-2026.html" style="color:var(--primary);">Extension Cost Guide 2026</a></h3><p>Read our local budget guide for South Derbyshire extension projects.</p></div></div>
<div class="service-card fade-in"><div class="service-card-body"><h3><a href="blog/do-you-need-planning-permission-for-an-extension-in-swadlincote.html" style="color:var(--primary);">Planning Permission Guide</a></h3><p>Understand when an extension may fall under permitted development and when to check further.</p></div></div>
<div class="service-card fade-in"><div class="service-card-body"><h3><a href="blog/how-to-choose-a-reliable-builder-in-swadlincote.html" style="color:var(--primary);">How to Choose a Reliable Builder</a></h3><p>A practical homeowner checklist for comparing builders and quotations.</p></div></div>
</div>
</div>
</section>
<!-- Stats Section -->'''
    old = '</section>\n<!-- Stats Section -->'
    if old not in text:
        raise RuntimeError('Expected insertion point not found in index.html')
    text = text.replace(old, block, 1)
    path.write_text(text, encoding='utf-8')


def update_sitemap():
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    urlset = ET.Element('{http://www.sitemaps.org/schemas/sitemap/0.9}urlset')
    priority_map = {
        'index.html': '1.0',
        'blog.html': '0.8',
        'portfolio.html': '0.7',
        'faq.html': '0.7',
        'referral.html': '0.7',
    }

    html_files = []
    for path in ROOT.rglob('*.html'):
        if '.git' in path.parts:
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith('node_modules/'):
            continue
        html_files.append(rel)

    for rel in sorted(html_files):
        url = ET.SubElement(urlset, '{http://www.sitemaps.org/schemas/sitemap/0.9}url')
        loc = ET.SubElement(url, '{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
        loc.text = f'{SITE}/{rel}'
        lastmod = ET.SubElement(url, '{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod')
        lastmod.text = DATE
        changefreq = ET.SubElement(url, '{http://www.sitemaps.org/schemas/sitemap/0.9}changefreq')
        changefreq.text = 'weekly'
        priority = ET.SubElement(url, '{http://www.sitemaps.org/schemas/sitemap/0.9}priority')
        if rel.startswith('services/'):
            priority.text = '0.9'
        elif rel.startswith('blog/'):
            priority.text = '0.8'
        elif rel in {href for _, href, _ in LANDING_PAGES}:
            priority.text = '0.85'
        else:
            priority.text = priority_map.get(rel, '0.7')

    tree = ET.ElementTree(urlset)
    tree.write(ROOT / 'sitemap.xml', encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    build_blog_html()
    update_homepage()
    update_sitemap()
    print('Updated blog.html, index.html, and sitemap.xml')
