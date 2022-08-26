import hidrocl
import hidrocl_paths as hcl
print(hidrocl.__version__)

pp = hidrocl.HidroCLVariable("pp",
                             hcl.pp_o_imerg_pp_mean_b_d_p0d,
                             hcl.pp_o_imerg_pp_mean_b_pc)

mcd15 = hidrocl.Gpm_3imrghhl(pp,
                             product_path=hcl.imerghhl_path,
                             vector_path=hcl.hidrocl_wgs84,
                             pp_log=hcl.log_pp_o_imerg_pp_mean)

mcd15.run_extraction()
