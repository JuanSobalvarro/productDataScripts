import pandas as pd
import matplotlib.pyplot as plt

def load_data(file_path):
    """
    Load product data from CSV.
    """
    return pd.read_csv(file_path)

def basic_statistics(df):
    """
    Calculate and print basic statistics, considering discounts.
    """
    total_products = df.shape[0]
    
    # Calculate average price considering discount
    df['EffectivePrice'] = df.apply(
        lambda row: row['Discount Value'] if row['With Discount'] else row['Price'], axis=1
    )
    average_price = df['EffectivePrice'].mean()
    
    in_stock_count = df['In Stock'].sum()
    out_of_stock_count = total_products - in_stock_count

    print("Estadisticas basicas:")
    print(f"Productos totales: {total_products}")
    print(f"Precio promedio: {average_price:.2f}")
    print(f"Productos en stock: {in_stock_count}")
    print(f"Productos fuera de stock: {out_of_stock_count}")
    print("-" * 50)


def price_distribution(df):
    """
    Plot the distribution of product prices.
    """
    plt.figure(figsize=(10, 6))
    plt.hist(df['Price'], bins=30, color='blue', alpha=0.7)
    plt.title('Distribucion de precio de productos')
    plt.xlabel('Precio')
    plt.ylabel('Frecuencia')
    plt.grid(axis='y', alpha=0.75)
    plt.show()

def stock_availability(df):
    """
    Calculate and plot the percentage of products in stock vs out of stock.
    """
    stock_counts = df['In Stock'].value_counts(normalize=True) * 100

    print("Porcentaje de productos en stock vs fuera de stock:")
    print(stock_counts)
    print("-" * 50)

    plt.figure(figsize=(8, 6))
    stock_counts.plot(kind='pie', autopct='%1.1f%%', colors=['green', 'red'], startangle=90)
    plt.title('Porcentaje de productos en stock vs fuera de stock')
    plt.ylabel('')  # Hide the y-label
    plt.show()

def correlation_price_quantity(df):
    """
    Calculate and plot the correlation between price and quantity.
    """
    correlation = df[['Price', 'Quantity']].corr().iloc[0, 1]
    print(f"Correlacion price y cantidad: {correlation:.2f}")
    
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Price'], df['Quantity'], alpha=0.6)
    plt.title('Precio vs Cantidad')
    plt.xlabel('Precio')
    plt.ylabel('Cantidad')
    plt.grid()
    plt.show()

def main():
    """
    Main function to run all analyses.
    """
    file_path = 'productsapi.csv'  # Path to your CSV file
    df = load_data(file_path)

    basic_statistics(df)
    price_distribution(df)
    stock_availability(df)
    correlation_price_quantity(df)

if __name__ == "__main__":
    main()
