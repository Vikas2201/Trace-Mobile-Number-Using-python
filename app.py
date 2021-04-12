from bs4 import BeautifulSoup
import mechanize as me
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index() :
    if request.method == 'POST':
        number = request.form['content'].replace(" ", "")
        try:
            mc = me.Browser()
            mc.set_handle_robots(False)
            # we using finddatatrace website for getting details of phone number
            url = "https://www.findandtrace.com/trace-mobile-number-location"
            mc.open(url)
            mc.select_form(name="trace")
            mc["mobilenumber"] = number
            res = mc.submit().read()
            # using Beautifulsoup
            bs = BeautifulSoup(res, "html.parser")
            table = bs.find_all("table", class_="shop_table")
            reviews = []
            data = table[0].find("tfoot")
            count = 0
            for i in data:
                count = count + 1
                if count in {1, 4, 6, 8}:  # for avoiding unnecessary data
                    continue
                table_h = i.find("th")
                table_d = i.find("td")
                reviews.append((table_h.text, table_d.text))
            data = table[1].find("tfoot")
            count = 0
            for i in data:
                count = count + 1
                if count in {2, 20, 22, 26}:
                    table_h = i.find("th")
                    table_d = i.find("td")
                    reviews.append((table_h.text, table_d.text))
            return render_template('results.html', reviews=reviews)
        except:
            return "please Enter Correct Information"
    else :
        return render_template('index.html')

if __name__ == "__main__":
    app.run(port=8000,debug=True)