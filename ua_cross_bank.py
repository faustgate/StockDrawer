import execjs
import requests
import lxml.html as html
import re


def get_rates():
    last_rate = None
    req = requests.get('http://minfin.com.ua/currency/mb/usd/').content
    xpath_query = ('/html/body/div[@class="mfz-page-wrap"]/div'
                   '/div[@class="mb-page clear"]'
                   '/div[@class="mb-main mb-main-300"]'
                   '/div/div[4]/div[@class="mb-graph clear"]'
                   '/div[@class="t-mrg fl goat-attack-left"]/script')
    scripts = html.fromstring(req).xpath(xpath_query)[0].text

# /html/body/div[@class="mfz-page-wrap"]/div/div[@class="mb-page clear"]/div[@class="mb-main mb-main-300"]/div/div[4]/div[@class="mb-graph clear"]/div[@class="t-mrg fl goat-attack-left"]/script
#
# /html/body/div[@class="mfz-page-wrap"]/div/div[@class="mb-page clear"]/div[@class="mb-main mb-main-300"]/div/div[4]/div[@class="mb-graph clear"]/div[@class="t-mrg fl goat-attack"]/script

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
    last_got_rate = rates[len(rates) - 1]
    if last_rate is None:
        last_rate = last_got_rate
        return rates
    if last_rate != last_got_rate:
        last_rate = last_got_rate
        return last_got_rate
    return None

if __name__ == '__main__':
    get_rates()