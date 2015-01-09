import execjs
import requests
import lxml.html as html
import re
from threading import Timer


def get_rates():
    req = requests.get('http://minfin.com.ua/currency/mb/usd/').content
    xpath_query = ('/html/body/div[@class="mfz-page-wrap"]/div/div[@class="mb-page clear"]/div[@class="mb-main mb-main-300"]/div/div[4]/div[1]/div[@class="t-mrg fl goat-attack"]/script')
    scripts = html.fromstring(req).xpath(xpath_query)[0].text

    fn_tpl = """
    function get_stock_rates(){
    0
    return ibusddayData;
    };
    """
    regexp_text = r'var ibusddayData(\s|\w|\.|\{|\}|=|\[|\]|,|:|"|;)*\];'
    regexp = re.compile(regexp_text)

    scripts2 = regexp.search(scripts)
    scr = scripts2.group()
    fn = fn_tpl.replace('0', scr)
    fun = execjs.compile(fn)
    rates = fun.call('get_stock_rates')
    last_rate = rates[len(rates) - 1]
    return last_rate
    # Timer(5.0, get_rates).start()


get_rates()