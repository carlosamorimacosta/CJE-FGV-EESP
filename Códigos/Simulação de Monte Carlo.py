import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Definindo o ticker e o período de interesse
ticker = 'WEGE3.SA'
start_date = '2022-06-12'
end_date = '2025-06-12'

# Baixar os dados de mercado
data = yf.download(ticker, start=start_date, end=end_date)

# Exibir as colunas disponíveis
print("Colunas disponíveis no dataset:")
print(data.columns)

# Exibir a estrutura inicial do dataframe
print("\nEstrutura inicial do dataframe:")
print(data.head())

# Definir a coluna de preço a ser usada para os cálculos (preço de fechamento)
price_column = ('Close', 'WEGE3.SA')

# Calcular os retornos diários (percentual de variação entre os preços de fechamento consecutivos)
data[('Return', '')] = data[price_column].pct_change()

# Exibir as colunas após a adição da coluna 'Return'
print("\nEstrutura após o cálculo dos retornos e verificação da coluna 'Return':")
print(data.head())

# Verificar as colunas do DataFrame
print("\nColunas do dataframe após o cálculo dos retornos:")
print(data.columns)

# Verificar se a coluna 'Return' foi criada corretamente
if ('Return', '') in data.columns:
    print("\nA coluna 'Return' foi criada com sucesso.")
else:
    print("\nA coluna 'Return' não foi criada corretamente.")

# Remover as linhas com valores NaN na coluna 'Return' após o cálculo dos retornos
# Garantir que estamos acessando a coluna 'Return' corretamente
data = data.dropna(subset=[('Return', '')])

# Exibir a estrutura do dataframe após a remoção dos NaN
print("\nEstrutura após a remoção dos NaN na coluna 'Return':")
print(data.head())

# Estatísticas necessárias
mean_return = data[('Return', '')].mean()  # Média dos retornos diários
std_return = data[('Return', '')].std()  # Desvio padrão dos retornos diários

# Exibir os resultados das estatísticas
print(f"\nMédia dos retornos diários: {mean_return:.6f}")
print(f"Desvio padrão dos retornos diários: {std_return:.6f}")

# Parâmetros da simulação
num_simulations = 10000
num_days = 252  # Um ano de negociação (aproximadamente 252 dias úteis)

# Inicialização para armazenar resultados das simulações
simulated_prices = np.zeros((num_simulations, num_days))
final_prices = np.zeros(num_simulations)

# Média e desvio padrão dos retornos diários
mean_return = data[('Return', '')].mean()
std_return = data[('Return', '')].std()

# Simulação de Monte Carlo
for i in range(num_simulations):
    # Simulado os preços para cada dia
    daily_returns = np.random.normal(mean_return, std_return, num_days)
    price_series = data[price_column].iloc[-1] * (1 + daily_returns).cumprod()
    simulated_prices[i, :] = price_series
    final_prices[i] = price_series[-1]

# Analisando os resultados
current_price = data[price_column].iloc[-1]

# Classificando os cenários
buy_count = np.sum(final_prices > current_price * 1.05)  # > 5% de aumento
hold_count = np.sum((final_prices <= current_price * 1.05) & (final_prices >= current_price * 0.95))  # -5% a +5%
sell_count = np.sum(final_prices < current_price * 0.95)  # <-5% de queda

# Porcentagens
buy_percentage = buy_count / num_simulations * 100
hold_percentage = hold_count / num_simulations * 100
sell_percentage = sell_count / num_simulations * 100

# Exibindo resultados
print(f"\nPorcentagem de Buy: {buy_percentage:.2f}%")
print(f"Porcentagem de Hold: {hold_percentage:.2f}%")
print(f"Porcentagem de Sell: {sell_percentage:.2f}%")

# Gráfico das simulações de preços
plt.figure(figsize=(10,6))
plt.plot(simulated_prices.T, color='lightgray', alpha=0.1)
plt.title(f"Simulações de Monte Carlo para o Preço da Ação da WEG ({ticker})")
plt.xlabel('Dias de Negociação')
plt.ylabel('Preço Simulado')
plt.show()

# Histograma com categorização Buy, Hold, Sell
plt.figure(figsize=(10, 6))

# Categorias com cores diferentes
plt.hist(final_prices[final_prices > current_price * 1.05], bins=50, alpha=0.6, label='Buy (> +5%)', color='green')
plt.hist(final_prices[(final_prices <= current_price * 1.05) & (final_prices >= current_price)], bins=50, alpha=0.6, label='Hold (0% a +5%)', color='blue')
plt.hist(final_prices[(final_prices < current_price * 0.95)], bins=50, alpha=0.6, label='Sell (< -5%)', color='red')

# Linha indicando o preço atual
plt.axvline(current_price, color='black', linestyle='--', label='Preço Atual')

# Título e legendas
plt.title(f'Histograma dos Preços Finais Simulados - WEG ({ticker})')
plt.xlabel('Preço Simulado no Fim do Período')
plt.ylabel('Frequência')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
