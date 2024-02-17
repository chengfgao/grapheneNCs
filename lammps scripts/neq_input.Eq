# 3d flow of Argon in Graphene Nanochannels simulation 
# Must use metal units for the rebo potential
# mpiexec -np 4 lmp_mpi -in in.Eq

dimension	3
boundary	p s p

atom_style	atomic

units metal

neighbor	0.2 bin
neigh_modify delay 0 check yes

# create geometry
read_data data.GraAr

# define groups
group flow type 1 #Argon
group upBoundary1 id 1:448 #Top Graphene1
group upBoundary2 id 449:896 #Top Graphene2
group downBoundary1 id 897:1344 #Bottom Graphene1
group downBoundary2 id 1345:1792 #Bottom Graphene2
group allGraphene type 2 

# Pair-Wise potential
# wall-fluid and fluid-fluid interacts with lj
# wall-wall uses rebo
pair_style	hybrid lj/cut 10 rebo
pair_coeff * *  rebo CH.airebo C C
#episilon=120K*Kb=0.01 eV for fluid-fluid
pair_coeff 1 1 lj/cut 0.01 3.4 10
pair_coeff 1 2 lj/cut 0.00483 3.4 10

# initial velocities
compute sys_temp all temp 
compute mobile_temp flow temp
velocity all create 120.0 31242 temp sys_temp 
velocity all zero linear

# Use langevin sys_thermostat
#damping paramter is set to 500 timesteps
fix sys_thermostat all langevin 120 120 0.5 525234 zero yes

# Time integration
fix t_integrate all nve

# Fix the COM of the Graphene
fix 4 upBoundary1 recenter INIT INIT INIT
fix 5 downBoundary1 recenter INIT INIT INIT
fix 6 upBoundary2 recenter INIT INIT INIT
fix 7 downBoundary2 recenter INIT INIT INIT

# deltat=1fs
timestep	0.001
thermo		100
thermo_modify temp mobile_temp

minimize 1.0e-4 1.0e-6 100 1000

#store values for visualization
#dump vis all custom 500 pos.equil id type xs ys zs
#run for 1ns
run 1000000

write_restart restart.equil



