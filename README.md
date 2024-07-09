1. Write a configuration file under directory ./confFiles
2. python launch_one_run.py ./confFiles/runxxx.mc.conf
Inside launch_one_run.py, the statistical part is launched using a subprocess after the mc computations finish.
3. Ensure that the equilibrium is reached for observable with observable_name in ./confFiles/runxxx.mc.conf,
and enough data points are collected, otherwise re-run launch_one_run.py ./confFiles/runxxx.mc.conf
4. cd ./data2json, python U_and_dist_data2json.py potential_function_name parameter_file_row
5. cd ./plt, use a python script to make plots. For example, for  potential_function_name=V2, parameter_file_row=row0
to make a plot: python V2_U_and_dist_json2plt.py row0