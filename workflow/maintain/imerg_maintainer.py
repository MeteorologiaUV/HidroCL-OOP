import hidrocl
import hidrocl.paths as hcl
print(hidrocl.__version__)

pp = hidrocl.HidroCLVariable("pp",
                             hcl.pp_o_imerg_pp_mean_b_d_p0d,
                             hcl.pp_o_imerg_pp_mean_b_pc)

imerg = hidrocl.Gpm_3imrghhl(pp,
                             product_path=hcl.imerghhl_path,
                             vector_path=hcl.hidrocl_wgs84,
                             pp_log=hcl.log_pp_o_imerg_pp_mean)

imerg.run_maintainer(hcl.log_file_maintainer)