# ms_thermo

Multi-species Thermodynamics tools.

This package can perform thermodynamic calculations involving multi species reacting gases. The exhaustive documentation can be found [here](http://open-source.pg.cerfacs.fr/ms_thermo).

Some functions of this package are accesible via command line:

 - tadia\_table _temperature_ _pressure_ _phi_ : returns adiabatic flame temperature and mass fractions of a kero-air mixture based on 2S\_KERO\_BFER table,
 - tadia\_cantera _temperature_ _pressure_ _phi_ _fuel\_name_ _cti\_file_ : returns adiabatic flame temperature and mass fractions of a fuel-air mixture based on a cantera file,
 - yk\_from\_phi _carbons\_in\_fuel_ _hydrogens\_in\_fuel_ _phi_ : returns mass fractions of species of a fuel-air mixture,
 - fresh\_gas _temperature_ _pression_ _phi_ : returns conservative variables (rho, rhoE, rhoYk) of the fresh gases of a kero-air mixture.
