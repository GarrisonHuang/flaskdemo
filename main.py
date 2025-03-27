from flask import Flask, render_template
from datetime import datetime
from scrape import scrape_stocks


# print(__name__)

app = Flask(__name__)

books = {
    1: {
        "name": "Python book",
        "price": 299,
        "image_url": "https://im2.book.com.tw/image/getImage?i=https://www.books.com.tw/img/CN1/136/11/CN11361197.jpg&v=58096f9ck&w=348&h=348",
    },
    2: {
        "name": "Java book",
        "price": 399,
        "image_url": "https://im1.book.com.tw/image/getImage?i=https://www.books.com.tw/img/001/087/31/0010873110.jpg&v=5f7c475bk&w=348&h=348",
    },
    3: {
        "name": "C# book",
        "price": 499,
        "image_url": "https://im1.book.com.tw/image/getImage?i=https://www.books.com.tw/img/001/036/04/0010360466.jpg&v=62d695bak&w=348&h=348",
    },
    4: {
        "name": "寶可夢 大絕招",
        "price": 1499,
        "image_url": "https://tw.portal-pokemon.com/assets_c/2018/09/banner_650x488_pokedex-thumb-650x488-12636.jpg",
    },
}


@app.route("/stocks")
def get_stocks():
    datas = scrape_stocks()

    for data in datas:
        print(data[0], data[1])
    return render_template("stocks.html", stocks=datas)


@app.route("/bmi/name=<name>&height=<h>&weight=<w>")
def get_bmi(name, h, w):
    try:
        bmi = round(eval(w) / (eval(h) / 100) ** 2, 2)
        return f"<h1><span style='color:blue'>{name}</span> BMI:{bmi}<h1>"
    except Exception as e:
        print(e)

    return "<h2>參數不正確</h2>"


@app.route("/sum/x=<x>&y=<y>")
def my_sum(x, y):

    # 參數不正確 請輸出參數錯誤 (try + except)
    try:
        total = eval(x) + eval(y)
        return f"<h1>{x}+{y}={total}</h1>"
    except Exception as e:
        print(e)

    return "<h2>參數不正確</h2>"


@app.route("/book/<int:id>")
def show_book(id):
    # 輸出有書<h1>第一本書:XXX</h1> 或 無此編號
    if id not in books:
        return f"<h2 style='color:red'>無此編號:{id}<h2>"

    return f"<h1>第{id}本書:{books[id]}</h1>"


@app.route("/books")
def show_books():
    print(books)

    for key in books:
        print(books[key])

    return render_template("books.html", books=books)


@app.route("/")
def index():
    today = datetime.now()
    print(today)

    # return f"<h1>Hello Flask!<br>{today}</h1>"
    name = "garrison"
    return render_template("index.html", date=today, name=name)


app.run(debug=True)  # 這句可以不用關server
