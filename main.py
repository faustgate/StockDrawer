import execjs
import requests
import lxml.html as html
import re
from threading import Timer


def get_rates():
    req = requests.get('http://minfin.com.ua/currency/mb/usd/').content
    scripts = html.fromstring(req).xpath('/html/body/div[2]'
                                         '/div/div[1]/div[1]'
                                         '/div/div[4]/div[1]'
                                         '/div[1]/script')[0].text

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
    last_rate = rates[len(rates)-1]
    return last_rate
    #Timer(5.0, get_rates).start()

get_rates()