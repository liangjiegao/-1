import requests

if __name__ == '__main__':
    url = "https://sogou.com/web"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    kw = input("请输入关键词：")
    params = {
        "query": kw
    }
    response = requests.get(url=url, params=params, headers=headers)
    text = response.text
    with open("./" + kw + ".html", "w", encoding="utf-8") as fp:
        fp.write(text)

    print("结束")