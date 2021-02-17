import argparse
import textwrap
import time
import urllib.request

from bs4 import BeautifulSoup


def contact():
    print("""
>>>> Contact <<<<
My Gmail: tucnakomet@gmail.com
My GitHub: https://github.com/tucnakomet1/
    """)


def exchange(From=None, To=None, Amount=None, whole=False):
    if From is None:
        return "Please enter the currency... For list of currencies: exchange.currencies()... For help: exchange.help()"
    if To is None:
        return "Please enter the currency... For list of currencies: exchange.currencies()... For help: exchange.help()"
    if Amount is None:
        Amount = 1

    url = f"https://www.x-rates.com/calculator/?from={From}&to={To}&amount={Amount}"
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")

    result = []
    INPUT = []

    for res in soup.findAll(attrs={"class": "ccOutputRslt"}):
        res = res.text.replace("\n", "")
        result.append(res)

    for inp in soup.findAll(attrs={"class": "ccOutputTxt"}):
        inp = inp.text.replace("\n", "")
        INPUT.append(inp)

    hard = ["".join(INPUT), "".join(result)]
    simple = result

    if not whole:
        return simple
    else:
        return hard


def currencies():
    hrefs = ["AUD - Australian Dollar", "BHD - Bahraini Dinar", "BWP - Botswana Pula", "BRL - Brazilian Real",
             "BND - Bruneian Dollar", "BGN - Bulgarian Lev", "CAD - Canadian Dollar", "CLP - Chilean Peso",
             "CNY - Chinese Yuan Renminbi", "COP - Colombian Peso", "HRK - Croatian Kuna", "CZK - Czech Koruna",
             "DKK - Danish Krone", "EUR - Euro", "HKD - Hong Kong Dollar", "HUF - Hungarian Forint",
             "ISK - Icelandic Krona", "INR - Indian Rupee", "IDR - Indonesian Rupiah", "IRR - Iranian Rial",
             "ILS - Israeli Shekel", "JPY - Japanese Yen", "KZT - Kazakhstani Tenge", "KRW - South Korean Won",
             "KWD - Kuwaiti Dinar", "LYD - Libyan Dinar", "MYR - Malaysian Ringgit", "MUR - Mauritian Rupee",
             "MXN - Mexican Peso", "NPR - Nepalese Rupee", "NZD - New Zealand Dollar", "NOK - Norwegian Krone",
             "OMR - Omani Rial", "PKR - Pakistani Rupee", "PHP - Philippine Peso", "PLN - Polish Zloty",
             "QAR - Qatari Riyal", "RON - Romanian New Leu", "RUB - Russian Ruble", "SAR - Saudi Arabian Riyal",
             "SGD - Singapore Dollar", "ZAR - South African Rand", "LKR - Sri Lankan Rupee", "SEK - Swedish Krona",
             "CHF - Swiss Franc", "TWD - Taiwan New Dollar", "THB - Thai Baht", "TTD - Trinidadian Dollar",
             "TRY - Turkish Lira", "AED - Emirati Dirham", "GBP - British Pound", "USD - US Dollar",
             "VEF - Venezuelan Bolivar"]
    return hrefs


def average(From=None, To=None, Amount=None, Year=None):
    if From is None:
        return "Please enter the currency... For list of currencies: exchange.currencies()... For help: exchange.help()"
    if To is None:
        return "Please enter the currency... For list of currencies: exchange.currencies()... For help: exchange.help()"
    if Amount is None:
        Amount = 1
    if Year is None:
        Year = time.strftime("%Y")
    elif int(Year) > int(time.strftime("%Y")) or int(Year) < int(time.strftime("%Y")) - 10:
        print(f"You can define 'year' only between {int(time.strftime('%Y')) - 10} - {time.strftime('%Y')}.")
        Year = time.strftime("%Y")

    url = f"https://www.x-rates.com/average/?from={From}&to={To}&amount={Amount}&year={Year}"
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")

    AvgMonth = []
    AvgRate = []
    AvgDays = []
    result = []

    for month in soup.findAll(attrs={"class": "avgMonth"}):
        month = month.text.replace("\n", "")
        AvgMonth.append(month)

    for rate in soup.findAll(attrs={"class": "avgRate"}):
        rate = rate.text.replace("\n", "")
        AvgRate.append(rate)

    for day in soup.findAll(attrs={"class": "avgDays"}):
        day = day.text.replace("\n", "")
        AvgDays.append(day)

    for i in range(0, len(AvgRate)):
        res = [AvgMonth[i], AvgRate[i], AvgDays[i]]
        result.append(res)

    return result


def help():
    print("""
        >>>> Welcome to currency-exchange help page! Whats wrong?! <<<<

-- version | 1.0.1
    


USAGE:

    >>> import currency_exchange

    ##### Get help #####
    >>> currency_exchange.help()

    ##### See license #####
    >>> currency_exchange.license()

    ##### Contact #####
    >>> currency_exchange.contact()


    ##### List of currencies #####
    >>> currency_exchange.currencies()

    ##### currency exchange#####
    >>> currency_exchange.exchange(from, to, amount, whole)

            # from = currency (ex: "USD", "EUR", "RUB", ...)
            # to = currency (ex: "USD", "EUR", "RUB", ...)
            # amount = number of amount (ex: 5, 14, 100, ...)
            # whole = True/False

    #### Monthly average #####
    >>> currency_exchange.average(from, to, amount, year)

            # from = currency (ex: "USD", "EUR", "RUB", ...)
            # to = currency (ex: "USD", "EUR", "RUB", ...)
            # amount = number of amount (ex: 5, 14, 100, ...)
            # year = number of CURRENT_YEAR to CURRENT_YEAR-10 (ex: 2020, 2015, 2010)
    


CONTACT:

    My Gmail: tucnakomet@gmail.com
    My GitHub: https://github.com/tucnakomet1/

    currency_exchange.contact()





LICENSE:

    MIT License: currency_exchange.license()
               : https://github.com/tucnakomet1/Python-Currency-Exchange/blob/master/LICENSE
    """)


def main():
    wrapper = textwrap.TextWrapper(width=70)
    string = wrapper.fill(
        text="Module 'currency-exchange' help you to find currency exchange and monthly currency average.")
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=string,
                                     epilog=textwrap.dedent("""
                                        Thank you!
                                        ↓  ↓  ↓  ↓
                                        Visit my GitHub: https://github.com/tucnakomet1
                                        """))
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0.1', help='show current version')
    parser.add_argument('-C', '--contact', action='store_true', help='show contact')
    parser.add_argument('-a', '--average', metavar="",
                        help='show currency monthly average. (ex: exchange -a "USD EUR 5 2020")')
    parser.add_argument('-e', '--exchange', metavar="", help='show currency exchange. (ex: exchange -e "USD EUR 5")')
    parser.add_argument('-c', '--currency', action="store_true", help='show all currency shortcuts')
    parser.add_argument('-w', '--whole', action='store_true', help='whole = True')

    args = parser.parse_args()

    if args.currency:
        print("\n".join(currencies()))

    if args.exchange:
        if args.whole:
            listOf = args.exchange.split()
            if len(listOf) == 1:
                print(exchange(listOf[0], whole=True))
            if len(listOf) == 2:
                print(" ".join(exchange(listOf[0], listOf[1], whole=True)))
            if len(listOf) == 3:
                print(" ".join(exchange(listOf[0], listOf[1], listOf[2], whole=True)))
            if len(listOf) > 3:
                print("Too much attributes...")

        else:
            listOf = args.exchange.split()
            if len(listOf) == 1:
                print(exchange(listOf[0]))
            if len(listOf) == 2:
                print(" ".join(exchange(listOf[0], listOf[1])))
            if len(listOf) == 3:
                print(" ".join(exchange(listOf[0], listOf[1], listOf[2])))
            if len(listOf) > 3:
                print("Too much attributes...")

    if args.average:
        avg = args.average.split()
        if len(avg) == 1:
            print(average(avg[0]))
        if len(avg) == 2:
            aver = average(avg[0], avg[1])
            for i in range(0, len(aver)):
                print(" ".join(aver[i]))

        if len(avg) == 3:
            aver = average(avg[0], avg[1], avg[2])
            for i in range(0, len(aver)):
                print(" ".join(aver[i]))
        if len(avg) == 4:
            aver = average(avg[0], avg[1], avg[2], avg[3])
            for i in range(0, len(aver)):
                print(" ".join(aver[i]))
        if len(avg) > 4:
            print("Too much attributes...")

    if args.contact:
        contact()


if __name__ == "__main__":
    main()
