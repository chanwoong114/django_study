from django.shortcuts import render

# Create your views here.

def price(request, thing, num):
    product_price = {"라면":980,"홈런볼":1500,"칙촉":2300, "식빵":1800}
    p = 0

    if thing in product_price:
        p = product_price[thing] * num

    context = {
        'product_price': product_price,
        'thing': thing,
        'num': num,
        'p': p
    }
    
    return render(request, 'prices/price.html', context)

product_price = {"라면":980,"홈런볼":1500,"칙촉":2300, "식빵":1800}
