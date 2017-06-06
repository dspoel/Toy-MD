# Toy-MD
This is a tiny repository with Python code to play with molecular
dynamics (MD) simulations. It can be extended for testing and
trying new algorithms or potentials. 

Disclaimer: the stuff in here is not suitable for production simulations.

Example for running:
% ./toy_md.py -h

This will give you the command line help for the script.

% cd carbon-dioxide
% ../toy_md.py -c co2.pdb -p params.txt
-f force_field.txt -w co2-output.pdb

And similar in the other directories.

Then open the resulting traj.pdb with a viewer of your choosing, but you can
use the simple PyMoL script for the purpose.

Enjoy Toy-MD!

