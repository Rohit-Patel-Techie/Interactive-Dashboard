import matplotlib.pyplot as plt
import seaborn as sns

def get_weather_data_from_main(df):
    print(df)
    #plot Temperature
    plt.figure(figsize = (6,4))
    sns.barplot(x = "city", y = "temperature", data = df)
    plt.xlabel("City")
    plt.ylabel("Temperature (°C)")
    plt.title("City Temperature")
    plt.tight_layout()
    plt.show()

    #Correlation Plot
    plt.figure(figsize=(6, 4))
    sns.scatterplot(
        x="temperature",
        y="humidity",
        data=df
    )
    plt.title("Temperature vs Humidity")
    plt.tight_layout()
    plt.show()