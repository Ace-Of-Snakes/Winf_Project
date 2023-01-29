# make a random array and plot it
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(0, 2*np.pi)
ax.set_ylim(-1, 1)

x = np.arange(0, 2*np.pi, 0.01)
line, = ax.plot(x, np.sin(x))

def animate(i):
    line.set_ydata(np.sin(x + i/10.0))  # update the data
    return line,

ani = animation.FuncAnimation(fig, animate, np.arange(1, 200), interval=25, blit=True)
plt.show()