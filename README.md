# Toy-MD
This is a tiny repository with Python code to play with molecular
dynamics (MD) simulations. It can be extended for testing and
trying new algorithms or potentials. 

Disclaimer: the stuff in here is not suitable for production simulations.

Example for running:
% ./toy_md.py -h

This will give you the command line help for the script.

% ./toy_md.py -c carbon-dioxide/co2.pdb -p carbon-dioxide/params.txt
-f carbon-dioxide/force_field.txt -w co2-output.pdb

Then open the resulting traj.pdb with a viewer of your choosing.
