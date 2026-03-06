import math

def calcular_motor(vazao,tensao):

    potencia_kw = vazao/1000*0.75

    corrente = round((potencia_kw*1000)/(1.73*tensao*0.85),2)

    disj = math.ceil(corrente*1.25)

    if corrente < 18:
        cabo = 2.5
    elif corrente < 28:
        cabo = 4
    elif corrente < 36:
        cabo = 6
    else:
        cabo = 10

    motor_cv = round(potencia_kw/0.736)

    return motor_cv,corrente,disj,cabo
