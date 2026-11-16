"""Generates a synthetic demo dataset -> data/laptops.csv
Replace data/laptops.csv with a real dataset (same column names) for real prices."""
import numpy as np, pandas as pd
rng = np.random.default_rng(42)
N = 1500
ram = rng.choice([4, 8, 16, 32, 64], N, p=[.1, .35, .35, .15, .05])
storage = rng.choice([128, 256, 512, 1024, 2048], N, p=[.05, .3, .4, .2, .05])
stype = rng.choice(["SSD", "HDD"], N, p=[.85, .15])
cpu = rng.choice(["Core i3 / Ryzen 3", "Core i5 / Ryzen 5", "Core i7 / Ryzen 7", "Core i9 / Ryzen 9"], N, p=[.2, .4, .3, .1])
gpu = rng.choice(["Integrated", "GTX 1650", "RTX 3050", "RTX 4060", "RTX 4070"], N, p=[.5, .15, .15, .12, .08])
screen = rng.choice([13.3, 14.0, 15.6, 16.0, 17.3], N)
res = rng.choice(["Full HD", "QHD or better"], N, p=[.7, .3])
brand = rng.choice(["Budget", "Mainstream", "Premium"], N, p=[.3, .45, .25])
lp = (10.31 + .18*np.log2(ram/8) + .12*np.log2(storage/256) + .08*(stype == "SSD")
      + pd.Series(cpu).map({"Core i3 / Ryzen 3": 0, "Core i5 / Ryzen 5": .15, "Core i7 / Ryzen 7": .32, "Core i9 / Ryzen 9": .5}).values
      + pd.Series(gpu).map({"Integrated": 0, "GTX 1650": .22, "RTX 3050": .38, "RTX 4060": .55, "RTX 4070": .75}).values
      + .02*(screen-15) + .1*(res == "QHD or better")
      + pd.Series(brand).map({"Budget": 0, "Mainstream": .1, "Premium": .25}).values
      + rng.normal(0, .06, N))
df = pd.DataFrame({"Brand": brand, "Ram_GB": ram, "Storage_GB": storage, "Storage_Type": stype,
                   "Processor": cpu, "GPU": gpu, "Screen_Size": screen, "Resolution": res,
                   "Price": np.round(np.exp(lp), -2)})
df.to_csv("data/laptops.csv", index=False)
print(df.shape); print(df.head())
