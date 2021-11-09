from flask import Flask, render_template, request
from num2words import num2words

app = Flask("__main__")

@app.route("/", methods = ["GET", "POST"])
def main_page():
    money_main = {
        "UAH_zero": "нуль","RUB_zero": "ноль","UAH_one": "один",  
        "RUB_one": "один","UAH_UAH": "гривня", "RUB_UAH": "гривна",  
        'RUB_USD': "долар",'RUB_EUR': "євро","USD": "долар", 
        "EUR": "євро","UAH_c": "копійка","RUB_c": "копейка", 
        "USD_c": "цент", "UAH_kilometer": "кілометр", "RUB_kilometer": "километр", 
        "UAH_kilometer_c": "метр", "RUB_kilometer_c": "метров", "UAH_meter": "метр", 
        "RUB_meter": "метр", "UAH_meter_c": "сантиметрів", "RUB_meter_c": "сантиметров", 
    }
    
    money_extended = {
        "UAH_two": "два", "RUB_two": "два", 'USD_UAH_c': "центів", 
        "UAH_UAH": "гривні", "RUB_UAH": "гривни", 'RUB_meter_RUB_c': "сантиметров", 
        'UAH_RUB_c': "копейок", 'USD_RUB_c': "центов", 'UAH_UAH_c': "центів", 
        'UAH_meter_UAH_c': "сантиметрів", "RUB_UAH_ext": "гривен", "USD": "долара", 
        "EUR": "євро", 'RUB_EUR': "євро", "UAH_c": "копійок", 
        "RUB_c": "копейок", "EUR_c": "центів", "EUR_RUB_c": "центов", 
        "USD_c": "центів", 'EUR_UAH_c': "центів", "RUB_USD_c": "центов", 
        "UAH_kilometer": "кілометри", "RUB_kilometer": "километр", "UAH_kilometer_c": "метри", 
        "UAH_meter": "метри", "RUB_meter": "метров", "UAH_meter_c": "сантиметрів", 
        "RUB_meter_c": "сантиметров", 'UAH_kilometer_UAH_c': "метри",'RUB_kilometer_c': "метра", 
        'RUB_kilometer_RUB_c': "метра", 
    }
    
    money_exception = {
        "UAH": "гривень", "RUB_UAH": "гривень", "USD": "доларів", 
        "RUB_USD": "доларов", "EUR": "євро", 'UAH_UAH_kilometer_c': "метрів", 
        'RUB_RUB_kilometer_c': "метров", "RUB_USD_c": "центов", 'UAH_EUR': "євро", 
        'UAH_EUR_c': "центів", 'UAH_UAH': "гривень", 'UAH_UAH_c': "копійок", 
        'UAH_USD': "доларів", 'UAH_USD_c': "центів", 'EUR_c': "центів", 
        'RUB_EUR_c': "центов", 'RUB_UAH_c': "копейок", "RUB_EUR": "євро", 
        "UAH_c": "копійок", "EUR_C": "центов", "RUB_c": "копейок", 
        "USD_c": "центів", "UAH_kilometer": "кілометрів", "RUB_kilometer": "километров", 
        "UAH_kilometer_c": "метрів", "RUB_kilometer_c": "метров", "UAH_meter": "метрів", 
        "RUB_meter": "метров", "UAH_meter_c": "сантиметрів", "RUB_meter_c": "сантиметров", 
        'RUB_RUB_meter_c': "сантиметра",'UAH_UAH_meter_c': "сантиметрів", 
    }

    def getWords(number, leng): #fucntion uses package num2words and represents it with words
        lenguages = {'UAH': 'uk', 'RUB': 'ru'}
        return num2words(float(number), lang = lenguages[leng], to = 'currency')

    if request.method == 'POST': 
        data = str(request.form.get('main_input', 0)).replace(",", ".") 
        data_splited = data.replace(" ", "", 1) if data.count(" ") == 2 else data

        money_dist = data_splited.split()[-1]
        #collecting form data
        if data_splited.split()[0] == '0':#if zero
            return f"<h1>0 {money_exception[request.form.get('lenguage', 'UAH') +'_'+money_dist]}</h1>"

        pre_comma = float(data_splited.split()[0])
        past_comma = str(pre_comma)[str(pre_comma).find(".")+1:]
        pre_comma = str(pre_comma)[:str(pre_comma).find(".")]

        if len(money_dist) > 3:
            money_dist = str(request.form.get('lenguage', 'UAH')) + "_" +money_dist
        past_comma += '00'
        if len(past_comma) > 3:
            past_comma = past_comma[:3]


        def res_vidminok(var, I): #function which chooses case of the word,also if kilometer
            if int(var) == 0:
                return ''

            if not 'kilometer' in data_splited.split()[-1] and I == 1:
                var = var[:2]

            if int(var) == 0: #case when 0.100 ...
                zero = money_main[request.form.get('lenguage', 'UAH') + "_zero"]
                if not past_comma:
                    return zero
                res = getWords(var, leng = request.form.get('lenguage', 'UAH'))
                result = res + money_exception[money_dist + '_c']
            
            
            elif int(var) == 1 or int(var[-1]) == 1 and not "11" in var: # case when number pre-comma ends with 1
                if "UAH" == money_dist:# special case for ukrainian
                    res = getWords(var, leng = request.form.get('lenguage', 'UAH'))
                    one = money_main[request.form.get('lenguage', 'UAH') + "_one"]
                    if I == 1: #past-comma part or number
                        result = res.replace("євро", money_main[money_dist + "_c"]).replace("евро", money_main[money_dist + "_c"])
                    else: result = res.replace("євро", money_main[request.form.get('lenguage', 'UAH') + '_' + money_dist]).replace("евро", money_main[request.form.get('lenguage', 'UAH') + '_' + money_dist])
                    if money_dist == 'UAH' and request.form.get('lenguage', 'UAH') == 'RUB':
                        result = "одна" + result[4:]
                else:#other cases
                    one = money_main[request.form.get('lenguage', 'UAH') + "_one"]
                    res = getWords(var, leng = request.form.get('lenguage', 'UAH'))
                    res = res[4:]
                    
                    if I == 1:#past-comma part or number
                        result = res.replace("євро", money_main[money_dist + "_c"]).replace("евро", money_main[money_dist + "_c"])
                    else: result = one + res.replace("євро", money_main[money_dist]).replace("евро", money_main[money_dist])

            elif int(var[-1]) == 2 and money_dist == 'UAH' and len(var) >= 2 and request.form.get('lenguage', 'UAH') == 'RUB':
                res = getWords(var, leng  =request.form.get('lenguage', 'UAH'))# case when number pre-comma ends with 2 and pre-comma len >=2 and leng is russian
                if I == 1: result = res + money_extended[request.form.get('lenguage', 'UAH') + "_two"] + " " + money_extended[money_dist + "_c"] + 'а'
                else:result = res.replace("евро", money_extended[request.form.get('lenguage', 'UAH') +'_'+ money_dist]).replace("два", "две")
                if money_dist == 'UAH' and request.form.get('lenguage', 'UAH') == 'RUB':
                    result = result.replace("гривни", "гривен")

            elif int(var[-1]) == 2 and money_dist != 'UAH' and len(var) >= 2:# case when number pre-comma ends with 2 and pre-comma len >=2
                res = getWords(var, leng = request.form.get('lenguage', 'UAH'))
                if I == 1: result = res + money_extended[request.form.get('lenguage', 'UAH') + "_two"] + " " + money_extended[money_dist + "_c"] + 'а'
                else: result = res.replace("євро", money_exception[money_dist]).replace("евро", money_exception[money_dist])
                print(pre_comma)
                if money_dist == 'UAH' and request.form.get('lenguage', 'UAH') == 'UAH' and pre_comma:
                    print(pre_comma)
                print(pre_comma)


            
            elif int(var[-1]) == 2 and money_dist != 'UAH' and len(var) < 2: # case when number pre-comma ends with 2 and pre-comma len <2
                if I == 1: result =  money_extended[request.form.get('lenguage', 'UAH') + "_two"] + " " + money_extended[money_dist + "_c"] + 'а'
                else: result =  money_extended[request.form.get('lenguage', 'UAH') + "_two"] + " " + money_extended[money_dist] + 'а'

        
            elif int(var[-1]) in range(1,5): #special cases for 2,3,4

                res = getWords(var, leng = request.form.get('lenguage', 'UAH'))

                if I==1:#past-comma part or number
                    print(money_dist + '_' + request.form.get('lenguage', 'UAH') + "_c")
                    result = res.replace("євро", money_extended[money_dist + "_c"]).replace("евро", money_extended[money_dist + "_" + request.form.get('lenguage', 'UAH') + "_c"])
                else: result = res.replace("євро", money_extended[request.form.get('lenguage', 'UAH') + '_' + money_dist]).replace("евро", money_extended[request.form.get('lenguage', 'UAH') + '_' + money_dist])
                print(pre_comma)
                if money_dist == 'UAH' and request.form.get('lenguage', 'UAH') == 'UAH' and pre_comma:
                    print(pre_comma)
                print(pre_comma)
            
            else: #other cases exp: 215646.11 ...
                res = getWords(var, leng = request.form.get('lenguage', 'UAH'))
                if I == 1:
                    result = res.replace("євро", money_exception[money_dist + "_c"]).replace("евро", money_exception[request.form.get('lenguage', 'UAH') + '_'+money_dist + "_c"])
                else:result = res.replace("євро", money_exception[money_dist]).replace("евро", money_exception[request.form.get('lenguage', 'UAH') + '_' + money_dist])
                print("LAST case", result)
            result = result[:result.find(",")]

            return result

        counter = 0 #variable to define pre-comma part and past-comma part
        res_number = res_vidminok(pre_comma, counter)
        counter += 1
        print("res_number", res_number)
        res_cell = res_vidminok(past_comma, counter)
        result = res_number + " " + res_cell #result
        return f"<h1> {result} </h1>"

    return render_template("main_page.html")



if __name__ == "__main__":
    app.run(debug=True)