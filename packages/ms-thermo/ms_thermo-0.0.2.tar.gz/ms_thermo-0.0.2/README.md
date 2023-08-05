# ms_thermo

This is the CERFACS minimal package for multispecies reactive operations. The exhaustive documentation can be found [here](http://open-source.pg.cerfacs.fr/ms_thermo).

## Installation 

Install from Python Package index:

```
pip install ms_thermo
```

## Command line tools 

Once the package is installed, you have acces in your terminal to the following shortcuts

### The `tadia_table` command

This returns the burnt gas temperature and mass fractions using a tabulation on Kerosene.
The tabulation was created using [CANTERA](https://cantera.org/).

A typical usage is, for a stoechiometric fresh gas mixture at ambiant conditions:

```
>tadia_table 300. 101325 1.


The adiabatic flame temperature of a mix C10H22-air from tables is : 2312.99 K.

Species     |    Mass fraction
------------------------------
N2          |       0.718
fuel        |       0.000
O2          |       -0.000
CO2         |       0.200
H2O         |       0.082
```

### The `tadia_cantera` command

This returns the burnt gas temperature and mass fractions using a CANTERA `.cti` file.

A typical usage is, for a stoechiometric fresh gas mixture at ambiant conditions:

```
>tadia_cantera 300 101325 1 NC10H22 ../../Desktop/Luche1.cti


**** WARNING ****
For species C5H4O, discontinuity in cp/R detected at Tmid = 1000
	Value computed using low-temperature polynomial:  22.0928
	Value computed using high-temperature polynomial: 22.1544

The adiabatic flame temperature of a mix C10H22-air from cantera is : 2277.41 K.

Species     |    Mass fraction
------------------------------
CO          |       0.014
CO2         |       0.172
H2O         |       0.084
N2          |       0.718
NO          |       0.003
O2          |       0.007
OH          |       0.002
+ 82 others |       0.000
```
**WARNING**: If you do not have CERFACS's CANTERA installed in your virtual environment, this function will not be available!!

### The `yk_from_phi` command

This returns the mass fractions of fresh gases according to chemical composition of the fuel and equivalence ratio.

Typical usage is :

```
>yk_from_phi 0.5 10. 22. 

Species     |    Mass fraction
------------------------------
fuel        |       0.466
N2          |       0.410
O2          |       0.125
```
### The `fresh_gas`command
This calculates the conservative variables of a Kerosene/air fresh gas mixture from primitive variables P, T and phi (equivalence ratio).

Typical usage is:

```
>fresh_gas 300 101325. 1.

rho       |  1.232 kg/m3
rhoE      |  266054.682 J.kg/m3
rhoYk     |
 N2       |  0.886 mol.kg/m3
 O2       |  0.269 mol.kg/m3
 KERO     |  0.077 mol.kg/m3
```
## Packages usage

The `ms_thermo` is also meant to be used in lager scripts/packages.

### The `state` class

The state class handles a mixture of gases.

Typical usage for this class . The following script creates an initial mixture of fresh gases, then changes a subset of the field into hot gases.

```
>>> import ms_thermo as ms
>>> case = ms.State()
>>> print(case)

Current primitive state of the mixture

		        | Most Common |    Min    |    Max 
----------------------------------------------------
             rho| 1.17192e+00 | 1.172e+00 | 1.172e+00 
          energy| 2.16038e+05 | 2.160e+05 | 2.160e+05 
     temperature| 3.00000e+02 | 3.000e+02 | 3.000e+02 
        pressure| 1.01325e+05 | 1.013e+05 | 1.013e+05 
            Y_O2| 2.32500e-01 | 2.325e-01 | 2.325e-01 
            Y_N2| 7.67500e-01 | 7.675e-01 | 7.675e-01 

>>> case.temperature = 1200
>>> print(case)

Current primitive state of the mixture 
			   	| Most Common |    Min    |    Max 
----------------------------------------------------
             rho| 2.92980e-01 | 2.930e-01 | 2.930e-01 
          energy| 9.41143e+05 | 9.411e+05 | 9.411e+05 
     temperature| 1.20000e+03 | 1.200e+03 | 1.200e+03 
        pressure| 1.01325e+05 | 1.013e+05 | 1.013e+05 
            Y_O2| 2.32500e-01 | 2.325e-01 | 2.325e-01 
            Y_N2| 7.67500e-01 | 7.675e-01 | 7.675e-01 


```


