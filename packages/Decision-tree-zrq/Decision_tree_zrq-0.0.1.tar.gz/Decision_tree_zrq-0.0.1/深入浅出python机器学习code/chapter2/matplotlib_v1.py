# %matplotlib inline
#激活matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
x=np.linspace(-20,20,10)
y=x**3+2*x**2+6*x+5
plt.plot(x,y,marker="o")
plt.show()