import pandas as pd
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
#Correlação de Parson entre a WEG3 e o valor do câmbio para o período entre janeiro de 2020 e janeiro de 2025
messes = [
    "jan/20", "fev/20", "mar/20", "abr/20", "mai/20", "jun/20", "jul/20", "ago/20", "set/20", "out/20", "nov/20", "dez/20",
    "jan/21", "fev/21", "mar/21", "abr/21", "mai/21", "jun/21", "jul/21", "ago/21", "set/21", "out/21", "nov/21", "dez/21",
    "jan/22", "fev/22", "mar/22", "abr/22", "mai/22", "jun/22", "jul/22", "ago/22", "set/22", "out/22", "nov/22", "dez/22",
    "jan/23", "fev/23", "mar/23", "abr/23", "mai/23", "jun/23", "jul/23", "ago/23", "set/23", "out/23", "nov/23", "dez/23",
    "jan/24", "fev/24", "mar/24", "abr/24", "mai/24", "jun/24", "jul/24", "ago/24", "set/24", "out/24", "nov/24", "dez/24",
    "jan/25"
]

usr_dbr1 = [
    4.282, 4.4733, 5.2046, 5.4858, 5.3361, 5.4661, 5.224, 5.4914, 5.6112, 5.7446, 5.3319, 5.1937,
    5.4625, 5.5986, 5.6315, 5.4366, 5.2172, 4.9686, 5.2123, 5.1492, 5.4428, 5.6372, 5.6239, 5.5703,
    5.3041, 5.1599, 4.739, 4.9721, 4.7315, 5.2562, 5.1734, 5.1831, 5.4154, 5.1791, 5.1851, 5.286,
    5.0731, 5.2367, 5.0631, 4.9865, 5.0574, 4.786, 4.7241, 4.9544, 5.032, 5.035, 4.9205, 4.8521,
    4.9526, 4.9716, 5.0153, 5.1934, 5.2443, 5.5925, 5.65, 5.6103, 5.4482, 5.7687, 5.9373, 6.1778,
    5.8415
]

enterprise_value = [
    72.604, None, None, 69.725, None, None, 106.2, None, None, 137.7, None, None,
    157.8, None, None, 154.3, None, None, 140, None, None, 164.7, None, None,
    137.8, None, None, 145.6, None, None, 111.5, None, None, 135.6, None, None,
    162.2, None, None, 169.6, None, None, 157.2, None, None, 150.5, None, None,
    153, None, None, 157.1, None, None, 174.3, None, None, 226.6, None, None,
    219.8
]

df = pd.DataFrame({
    'mes': messes,
    'usr_dbr1': usr_dbr1,
    'enterprise_value': enterprise_value
})

# Remove links from valores faltantes
df_limpo = df.dropna()

# Calculate correlação de Pearson
correlacao, p_valor = pearsonr(df_limpo['usr_dbr1'], df_limpo['enterprise_value'])

print(f"Correlação de Pearson: {correlacao:.4f}")
print(f"p-valor: {p_valor:.4f}")

# (Opcional) Visualizar a relação
plt.figure(figsize=(10, 6))
plt.scatter(df_limpo['usr_dbr1'], df_limpo['enterprise_value'], color='blue')
plt.xlabel('USD/BRL')
plt.ylabel('Enterprise Value ($ bi)')
plt.title('Correlação entre Câmbio e Enterprise Value')
plt.grid(True)
plt.show()
