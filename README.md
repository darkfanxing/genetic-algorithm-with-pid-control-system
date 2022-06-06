# Genetic Algorithm with PID Control system
## 1. Control System I used
### 1.1 Control System
![](https://i.imgur.com/uD6GOUn.png)

### 1.3 The Input of The Control System
- 4 periods of standard rectangular signal
- Each period was cut into 60 pieces (ticks)

### 1.2 The Output And PID Setting of The Control System
![](https://i.imgur.com/aAwXYRa.png)

## 2. Execute Project
### 2.1 Environment Setup
```
pip install pipenv
pipenv shell --python 3.9
pipenv install
```

### 2.2 Run the Project
Open the `src/main.ipynb` file, and run all cells

## 3. Results
The result table is based on the following settings of genetic algorithm:
1. `population number`: 50
2. `iteration number`: 100
3. `mutation probability`: 0.1
4. `crossover rate`: 0.9
5.  `PID value boundary`: [0, 1]
6.  `eta value boundary`: [0.30001, 0.69999]
7.  `fitness function`:

    ![](https://i.imgur.com/y0XF8TL.png?)


| Control System Output                | Chromosome Value                                     | Control System Setting                          |
| --                                   | --                                                   | --                                              |
| ![](https://i.imgur.com/PpCHRmo.png) | P / I / D / eta:<br />0.990 / 0.249 / 0.021 / 0.3001 | initial_y_now / u_boundary:<br />-2 / [-20, 20] |
| ![](https://i.imgur.com/WvvNBCY.png) | P / I / D / eta:<br />1.000 / 0.301 / 0.025 / 0.3001 | initial_y_now / u_boundary:<br />0 / [-20, 20]  |
| ![](https://i.imgur.com/MIhFG1P.png) | P / I / D / eta:<br />1.000 / 0.269 / 0.012 / 0.3001 | initial_y_now / u_boundary:<br />2 / [-20, 20]  |
| ![](https://i.imgur.com/r45zWmu.png) | P / I / D / eta:<br />0.938 / 0.249 / 0.030 / 0.3001 | initial_y_now / u_boundary:<br />-2 / [-50, 50] |
| ![](https://i.imgur.com/tMVETpy.png) | P / I / D / eta:<br />1.000 / 0.257 / 0.000 / 0.3001 | initial_y_now / u_boundary:<br />0 / [-50, 50]  |
| ![](https://i.imgur.com/EPgnP2n.png) | P / I / D / eta:<br />1.000 / 0.251 / 0.006 / 0.3001 | initial_y_now / u_boundary:<br />2 / [-50, 50]  |
