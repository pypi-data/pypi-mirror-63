import sys
from pathlib import Path


# create logger
import os
import logging
from .main_logging import configure_colored_logger

os.system('COLOR 08')

logging.basicConfig(level=logging.INFO)
configure_colored_logger(remove_existing_handlers=True, level=logging.INFO)

module_logger = logging.getLogger('fipt')
module_logger.setLevel(logging.DEBUG)


# Load fipt analysis
import pandas as pd
import fipt


fn = sys.argv[1]
assert Path(fn).exists()

module_logger.info(f'Loading {fn}')

df = pd.read_csv(fn)
ipdata =  fipt.ImpedanceData(fn, fn, 
                   f_data = df.iloc[:, 0].values,  
                   z_real_data = df.iloc[:, 1].values, 
                   z_imag_data = df.iloc[:, 2].values)


symimfit = fipt.SymmetricImpedanceFitter(impedance_data=ipdata)        
symimfit.sanitize_data()

# restrict data range
symimfit.set_min_w(None)
symimfit.set_max_z_abs(400)

# use student t likelihood function
symimfit.configure_likelihood(likelihood_config=dict(name='t', scale=1, df=1))

# guess start parameters
start_params = symimfit.guess(make_plots=False)

result = symimfit.fit()        

fit_report_str = fipt.lmfit.fit_report(result, show_correl=False)
module_logger.info(fit_report_str)

f, ax = symimfit.plot_fit(start_params = start_params);
# f.show()

result_fns = symimfit.save_results()

for result_fn in result_fns:
    if result_fn:
        module_logger.info(f'Result written to {result_fn}')


