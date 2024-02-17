log 21_Self_K=2_Thermo_Traj4.lammps
# 3d flow of Argon in Graphene Nanochannels simulation 
# Must use metal units for the rebo potential
# mpiexec -np 4 lmp_mpi -in 21_in_Con.Eq

dimension	3
boundary	p s p

atom_style	atomic

units metal

neighbor	0.2 bin
neigh_modify delay 0 check yes

# create geometry
read_restart 21_Self_K=002_Ntraj5.restart

# define groups
group flow type 1 #Argon
group upBoundary1 id 1:448 #Top Graphene1 #y=0
group upBoundary2 id 449:896 #Top Graphene2 #y=3.4
group upBoundary id 1:896
group downBoundary1 id 897:1344 #Bottom Graphene1 #y=24.4
group downBoundary2 id 1345:1792 #Bottom Graphene2 #y=27.8
group downBoundary id 897:1792
group Allgraphene type 2 
group InnerGraphene id 449:1344

# Pair-Wise potential
# wall-fluid and fluid-fluid interacts with lj
# wall-wall uses rebo
pair_style	hybrid lj/cut 10 rebo
#type 1 is argon and type 2 is carbon
pair_coeff * *  rebo CH.airebo NULL C

#episilon=120K*Kb=0.01 eV for fluid-fluid
pair_coeff 1 1 lj/cut 0.01 3.4 10
pair_coeff 1 2 lj/cut 0.00483 3.4 10

pair_modify pair rebo compute/tally no
pair_modify pair lj/cut compute/tally yes

# Fix the Graphene to total COM or self COM
fix sta Allgraphene spring/self 0.02

# Use langevin sys_thermostat
#damping paramter is set to 500 timesteps
#eta = 0.2/0.0005 = 400, 1/0.0005=2000


#'''compute change of energy in 3 dimensions independently for two InnerGraphene'''
compute wall1_temp_yz upBoundary2 temp/partial 0 1 1
compute wall2_temp_yz downBoundary1 temp/partial 0 1 1
fix langevin_1_yz upBoundary2 langevin 120 120 2 7142 tally yes zero yes 
fix_modify langevin_1_yz temp wall1_temp_yz
fix_modify langevin_1_yz energy yes
fix langevin_2_yz downBoundary1 langevin 120 120 2 682341 tally yes zero yes 
fix_modify langevin_2_yz temp wall2_temp_yz
fix_modify langevin_2_yz energy yes
#'''Now the x-component'''
compute wall1_temp_x upBoundary2 temp/partial 1 0 0
compute wall2_temp_x downBoundary1 temp/partial 1 0 0
fix langevin_1_x upBoundary2 langevin 120 120 2 7142 tally yes zero yes
fix_modify langevin_1_x temp wall1_temp_x
fix_modify langevin_1_x energy yes
fix langevin_2_x downBoundary1 langevin 120 120 2 682341 tally yes zero yes 
fix_modify langevin_2_x temp wall2_temp_x
fix_modify langevin_2_x energy yes
#'''Deal with two outerwalls separetely'''
compute upBoundary1_temp upBoundary1 temp
compute downBoundary2_temp downBoundary2 temp
fix langevin_upBoundary1 upBoundary1 langevin 120 120 2 925883 zero yes
fix langevin_downBoundary2 downBoundary2 langevin 120 120 2 77512 zero yes  

#'''compute change of energy in 3 dimensions altogther'''
#compute wall1_temp upBoundary temp
#compute wall2_temp downBoundary temp
#fix langevin_1 upBoundary2 langevin 120 120 10 7142 tally yes zero yes 
#fix langevin_1_prime upBoundary1 langevin 120 120 10 925883 zero yes 
#fix_modify langevin_1 energy yes
#fix langevin_2 downBoundary1 langevin 120 120 10 682341 tally yes zero yes 
#fix langevin_2_prime downBoundary2 langevin 120 120 10 77512 zero yes 
#fix_modify langevin_2 energy yes

# Time integration
fix t_integrate all nve

#compute specific potential energies
compute 0 all pair rebo
variable REBO     equal c_0[1]
compute 1 all pair lj/cut
variable elj    equal c_1

compute mobile_temp flow temp
compute wall1_temp upBoundary2 temp
compute wall2_temp downBoundary1 temp


# deltat=1fs 0.001
timestep	0.0005
thermo		5000

#thermo_style custom step c_wall_temp c_mobile_temp etotal ke v_REBO v_elj f_13  
thermo_style custom step c_wall1_temp c_wall2_temp c_mobile_temp etotal ke v_REBO v_elj
#run 2000000

#compute friction of liquid due to Graphene
#compute friction flow force/tally InnerGraphene
#dt=2 or dt=5
#dump fri_force flow custom 5 21_Self_K=002_eta=1ps_fri_NTraj5.dump id x y z c_friction[1]

#record graphene position
#dump graphene_pos InnerGraphene custom 25 21_COM_K=5_eta=1ps_Graphene_NTraj1.dump id x y z

#record energy changed by langevin thermostat
fix dQ_langevin_1_partial upBoundary2 ave/time 1 1 1 f_langevin_1_yz f_langevin_1_x file XYZ_Traj1_21_K=002_Wall1_eta=2ps_dQ
fix dQ_langevin_2_partial downBoundary1 ave/time 1 1 1 f_langevin_2_yz f_langevin_2_x  file XYZ_Traj1_21_K=002_Wall2_eta=2ps_dQ

#fix dQ_langevin_1 upBoundary2 ave/time 1 1 1 f_langevin_1 file TEST_XYZ_Traj1_21_K=002_Wall1_eta=10ps_dQ
#fix dQ_langevin_2 downBoundary1 ave/time 1 1 1 f_langevin_2  file TEST_XYZ_Traj1_21_K=002_Wall2_eta=10ps_dQ

#run for 5ns 5000000
run 5000000

write_restart 21_Self_TEST_XYZ_K=002_traj1.restart


