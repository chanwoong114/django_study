from django.shortcuts import render

# Create your views here.
def input(request):
    return render(request, 'calculator/input.html')

def output(request):
    number1 = request.GET.get('number1')
    number2 = request.GET.get('number2')

    number_sub = int(number1) - int(number2)
    if number2 != '0':  number3 = int(number1)/int(number2) 
    else: number3 =  0

    context = {
        'number1': number1,
        'number2': number2,
        'number3' : number3,
        'number_sub': number_sub
    }

    return render(request, 'calculator/output.html', context)

def cal(request, no1, no2):
    add = no1 + no2
    sub = no1 - no2
    mul = no1 * no2
    if no2 != 0:
        div = no1 / no2
    else:
        div = '0'

    context = {
        'no1': no1,
        'no2': no2,
        'add': add,
        'sub': sub,
        'mul': mul,
        'div': div,
    }
    
    return render(request, 'calculator/cal.html', context)