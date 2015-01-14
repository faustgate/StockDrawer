import execjs
import requests
import lxml.html as html
import re


def get_rates():
    last_rates = {}
    currencys = ['usd', 'eur', 'rub']
    fn_tpl = """
    function get_stock_rates(){
    stock_rates = 0
    return stock_rates;
    };
    """
    regexp = re.compile(r'\[(\s|\w|\.|\{|\}|=|\[|\]|,|:|"|;)*\];')
    result = {}

    xpath_queries = {'cross': ('/html/body/div[@class="mfz-page-wrap"]/div'
                               '/div[@class="mb-page clear"]'
                               '/div[@class="mb-main mb-main-300"]'
                               '/div/div[4]/div[@class="mb-graph clear"]'
                               '/div[@class="t-mrg fl goat-attack-left"]'
                               '/script'),
                     'market': ('/html/body/div[@class="mfz-page-wrap"]/div'
                                '/div[@class="mb-page clear"]'
                                '/div[@class="mb-main mb-main-300"]'
                                '/div/div[4]/div[@class="mb-graph clear"]'
                                '/div[@class="t-mrg fl goat-attack"]'
                                '/script')}
    for cur in currencys:
        req = requests.get('http://minfin.com.ua/currency/mb/' + cur).content
        for query in xpath_queries:
            res_key = '{0}_{1}'.format(cur, query)
            scripts = html.fromstring(req).xpath(xpath_queries[query])[0].text
            scripts2 = regexp.search(scripts)
            scr = scripts2.group()
            fn = fn_tpl.replace('0', scr)
            fun = execjs.compile(fn)
            rates = fun.call('get_stock_rates')
            last_got_rate = rates[len(rates) - 1]
            last_rates[res_key] = last_got_rate
            result[res_key] = rates
    return result


if __name__ == '__main__':
    get_rates()