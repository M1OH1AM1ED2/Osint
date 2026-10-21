from flask import Flask ,render_template,request,jsonify
from playwright.sync_api import sync_playwright
app = Flask(__name__)
def classify_set(link,titel):
    link_lower= link.lower() if link else  ''
    titel_lower= titel.lower() if titel else ''
    social_sites = {
        "Facebook":['facebook.com','facebook'],
        "Youtube":['youtube.com',"youtube", "yt","youtu.be"],
        "Telegram":['telegram.org',"t.me/","telegram"],
        "instagram":['instagram','insta']
    }
    for site , keyword in social_sites.items():
        if any(k in link_lower or k in titel_lower for k in keyword):
            return site 
    educatino_site = {
        "udemy":['udemy.com'],
        'Coursera':['corsera.org','coursera']
    }
    for site , keyword in educatino_site.items():
        if any(k in link_lower or k in titel_lower for k in keyword):
            return site 
    news_site= ['2M.com']
    if any(k in link_lower or k in titel_lower for k in news_site):
        return "New Sites"
    if any(email_word in titel_lower for email_word in ["@","mail"]):
        return "Emails"
    if any (phone_namber in titel_lower for phone_namber in ['phone','mobiel','+34']):
        return "Phone Numbers"
    official_site = ['.edu','org','gov','ma']
    if any (k in titel_lower for k in official_site):
        return "Official set"
    general_sites = [
        'gethub.io','getlab.com','trayhakme'
    ]
    if any (k in link_lower or k in titel_lower for k in general_sites ):
        return "websites"
    return 'Website'
def osint_ex(query):
    try:
        with sync_playwright( ) as pr :
            browser = pr.chromium.launch(headless=True)
            contex = browser.new_context()
            page = browser.new_page()
            serach_link = f"https://duckduckgo.com/?q={query}&t=_&ia=web"       
            page.goto(serach_link,timeout=40000,wait_until='load')
            num_page = 2 
            All_results = []
            for _ in range(num_page):
                page.wait_for_selector('article[data-testid="result"]',timeout=20000)
                results= page.query_selector_all('article[data-testid="result"]')
                for result in results :
                    try:
                        titel_elemint = result.query_selector('h2 a')
                        link_element = result.query_selector('h2 a')
                        image_lelment= result.query_selector('img')
                        if titel_elemint and link_element:
                            title = titel_elemint.inner_text()
                            link = link_element.get_attribute('href')
                            image_element = result.query_selector('img')
                            image = image_element.get_attribute('src') if image_element else None
                            site_type = classify_set(link,title)
                            All_results.append(
                                {
                                    "title":title,
                                    "link":link,
                                    "image":image,
                                    "type":site_type,
                                }
                            )
                    except Exception:
                        continue
                next_btn = page.query_selector('button#more-results')
                if next_btn:
                    next_btn.click()
                    page.wait_for_timeout(9000)
                else:
                    break
            browser.close()
            return All_results
    except Exception as e :
        print(f"Error found :{e}")
        return[]
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/search',methods=["POST"])
def search():
    query =  request.form.get('query')
    resultsx = osint_ex(query)
    return jsonify(resultsx)
if __name__ == '__main__':
    app.run(debug=False,use_reloader=False)
