import streamlit as st

# Função para calcular impostos e valores relacionados
def calcular_impostos(faturamento, beneficios):
    faturamento_anual = faturamento * 12

    # Verificando a alíquota do Simples Nacional
    if faturamento_anual <= 4800000:
        if faturamento_anual <= 180000:
            aliquota_simples_nacional = 0.06
            deducao = 0
        elif faturamento_anual <= 360000:
            aliquota_simples_nacional = 0.1120
            deducao = 9360
        elif faturamento_anual <= 720000:
            aliquota_simples_nacional = 0.1350
            deducao = 17640
        elif faturamento_anual <= 1800000:
            aliquota_simples_nacional = 0.16
            deducao = 35640
        elif faturamento_anual <= 3600000:
            aliquota_simples_nacional = 0.21
            deducao = 125640
        else:
            aliquota_simples_nacional = 0.33
            deducao = 648000
    else:
        st.write("Faturamento não enquadrado no Simples Nacional - ME.")
        return

    # Calculando fator R
    fator_r = 0.28

    # Calculando contribuição patronal
    if faturamento_anual <= 3600000:
        cpp = 0.4340 * aliquota_simples_nacional * faturamento
    else:
        cpp = 0.3050 * aliquota_simples_nacional * faturamento

    # Calculando Pro Labore
    pro_labore = fator_r * faturamento

    # Calculando INSS
    inss = 0.11 * (pro_labore - cpp)

    # Calculando IRRF
    base_calculo = pro_labore - inss
    if base_calculo <= 2259.20:
        irrf = 0
        deducao_irrf = 0
    elif base_calculo <= 2826.65:
        irrf = 0.075
        deducao = 169.44
    elif base_calculo <= 3751.05:
        irrf = 0.15
        deducao = 381.44
    elif base_calculo <= 4664.68:
        irrf = 0.225
        deducao = 662.77
    else:
        irrf = 0.275
        deducao = 896

    irrf = (irrf * base_calculo) - deducao

    # Calculando o total de impostos
    impostos_pj = aliquota_simples_nacional * faturamento
    total_impostos = impostos_pj + inss + irrf - deducao

    # Calculando o salário líquido
    salario_liquido = faturamento - total_impostos
    salario_liquido_beneficios = salario_liquido + beneficios

    # Calculando a alíquota efetiva
    aliquota_efetiva = (total_impostos / faturamento) * 100

    return {
        "Impostos pagos na PJ": impostos_pj,
        "Contribuição Patronal": cpp,
        "Impostos pagos na PF (sobre o Pro Labore)": inss + irrf,
        "Total de Impostos": total_impostos,
        "Salário Líquido": salario_liquido,
        "Salário Líquido + Benefícios": salario_liquido_beneficios,
        "Alíquota Efetiva (%)": aliquota_efetiva
    }

# Interface com o usuário
st.title("Calculadora de Imposto PJ para Profissionais de TI")
st.write("Esta ferramenta calcula os impostos e o salário líquido para profissionais de TI enquadrados no Simples Nacional.")

faturamento = st.number_input("Faturamento Mensal (R$)", min_value=0.0, format="%.2f")
beneficios = st.number_input("Valor dos Benefícios (R$)", min_value=0.0, format="%.2f")

if st.button("Calcular"):
    resultados = calcular_impostos(faturamento, beneficios)
    if resultados:
        st.write(f"**Impostos pagos na PJ:** R$ {resultados['Impostos pagos na PJ']:.2f}")
        st.write(f"**Contribuição Patronal:** R$ {resultados['Contribuição Patronal']:.2f}")
        st.write(f"**Impostos pagos na PF (sobre o Pro Labore):** R$ {resultados['Impostos pagos na PF (sobre o Pro Labore)']:.2f}")
        st.write(f"**Total de Impostos:** R$ {resultados['Total de Impostos']:.2f}")
        st.write(f"**Salário Líquido:** R$ {resultados['Salário Líquido']:.2f}")
        st.write(f"**Salário Líquido + Benefícios:** R$ {resultados['Salário Líquido + Benefícios']:.2f}")
        st.write(f"**Alíquota Efetiva:** {resultados['Alíquota Efetiva (%)']:.2f}%")
