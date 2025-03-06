import streamlit as st
import pandas as pd

def calculate_cost(fca_price, quantity, logistics, duty_rate, vat_rate):
    fca_total = fca_price * quantity
    duty = (fca_total * duty_rate) / 100
    vat = ((fca_total + duty + logistics) * vat_rate) / 100
    ddp_total = fca_total + logistics + duty + vat
    return fca_total, ddp_total

# Загрузка данных прайс-листа
file_path = "Прайс Экспорт1.xlsx"
df = pd.read_excel(file_path, sheet_name="Лист1", skiprows=2)
df.columns = ["Продукция", "Тип упаковки", "Вес нетто (кг)", "Кол-во в ящике", "Ящиков на паллете", "Срок годности", "Цена FCA (грн)", "Цена FCA (EUR)", "Курс"]

st.title("Оптовый калькулятор стоимости продукции Yagodar")

# Выбор продукции
product = st.selectbox("Выберите продукцию", df["Продукция"].dropna().unique())
selected_row = df[df["Продукция"] == product].iloc[0]

fca_price = selected_row["Цена FCA (EUR)"]
quantity = st.number_input("Количество (ящики)", min_value=1, step=1)
logistics = st.number_input("Логистика (€)", min_value=0.0, step=1.0)
duty_rate = st.number_input("Импортные пошлины (%)", min_value=0.0, max_value=100.0, step=0.1, value=10.0)
vat_rate = st.number_input("НДС (%)", min_value=0.0, max_value=100.0, step=0.1, value=20.0)

if st.button("Рассчитать"):
    fca_total, ddp_total = calculate_cost(fca_price, quantity, logistics, duty_rate, vat_rate)
    st.write(f"**Стоимость FCA:** {fca_total:.2f} €")
    st.write(f"**Стоимость DDP:** {ddp_total:.2f} €")
