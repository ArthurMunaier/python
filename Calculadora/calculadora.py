import math
from flask import render_template, request


def calcular():

    num1 = float(request.form["num1"])
    operacao = request.form["operacao"]

    if operacao == "sqrt":
        if num1 < 0:
            resultado = "Erro: número negativo"
            etapas = f"Não existe raiz real de {num1}."
        else:
            resultado = math.sqrt(num1)
            etapas = f"√{num1} = {resultado}"

    elif operacao == "log":
        if num1 <= 0:
            resultado = "Erro"
            etapas = "Logaritmo só existe para números positivos."
            
        else:
            resultado = math.log10(num1)
            etapas = f"log({num1}) = {resultado}"
            
    elif operacao == "bhaskara":

        num2 = float(request.form["num2"])
        num3 = float(request.form["num3"])

        a = num1
        b = num2
        c = num3

        delta = (b ** 2) - (4 * a * c)

        if delta < 0:

            resultado = "Erro"

            etapas = (
                f"Δ = {delta}. "
                "Não existem raízes reais."
            )

        else:

            x1 = (-b + math.sqrt(delta)) / (2 * a)

            x2 = (-b - math.sqrt(delta)) / (2 * a)

            resultado = (
                f"x1 = {x1} | x2 = {x2}"
            )

            etapas = (
                f"Δ = {b}² - 4×{a}×{c} = {delta}"
            )

    else:

        num2_valor = request.form.get(
            "num2",
            ""
        ).strip()

        if not num2_valor:

            return render_template(
                "calculadora.html",
                etapas="Informe o segundo número para esta operação.",
                resultados="",
            )

        num2 = float(num2_valor)

        if operacao == "+":

            resultado = num1 + num2

            etapas = (
                f"{num1} + {num2} = {resultado}"
            )

        elif operacao == "-":

            resultado = num1 - num2

            etapas = (
                f"{num1} - {num2} = {resultado}"
            )

        elif operacao == "*":

            resultado = num1 * num2

            etapas = (
                f"{num1} × {num2} = {resultado}"
            )

        elif operacao == "/":

            if num2 == 0:

                resultado = "Erro"

                etapas = (
                    "Não existe divisão por zero."
                )

            else:

                resultado = num1 / num2

                etapas = (
                    f"{num1} ÷ {num2} = {resultado}"
                )

        elif operacao == "**":

            resultado = math.pow(num1, num2)

            etapas = (
                f"{num1}^{num2} = {resultado}"
            )

        else:

            resultado = "Operação inválida"

            etapas = "Escolha uma operação válida."

    return render_template(
        "calculadora.html",
        etapas=etapas,
        resultados=resultado,
    )

