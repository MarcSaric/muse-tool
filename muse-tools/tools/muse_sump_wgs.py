import os
import sys
from cdis_pipe_utils import df_util
from cdis_pipe_utils import pipe_util
from cdis_pipe_utils import time_util

def sump_wgs(uuid, muse_call_output_path, dbsnp_known_snp_sites, engine, logger):
  sump_dir = os.path.dirname(muse_call_output_path)
  input_name = os.path.basename(muse_call_output_path)
  input_base, input_ext = os.path.splitext(input_name)
  sample_base, sample_ext = os.path.splitext(input_base)
  logger.info('MuSE_sump_dir=%s' % sump_dir)
  step_dir = sump_dir
  muse_sump_output = input_base + '.vcf'
  muse_sump_output_path = os.path.join(sump_dir, muse_sump_output)
  logger.info('muse_sump_output_path=%s' % muse_sump_output_path)
  if pipe_util.already_step(step_dir, sample_base + '_MuSE_sump', logger):
    logger.info('already completed step `MuSE sump` of: %s' % input_name)
  else:
    logger.info('running step `MuSE sump` of the tumor bam: %s' % input_name)
    home_dir = os.path.expanduser('~')
    muse_path = os.path.join(home_dir, 'tools', 'MuSEv1.0rc_submission_c039ffa')
    cmd = [muse_path, 'sump', '-I', muse_call_output_path, '-G', '-O', muse_sump_output_path, '-D', dbsnp_known_snp_sites]
    output = pipe_util.do_command(cmd, logger)
    df = time_util.store_time(uuid, cmd, output, logger)
    df['muse_call_output'] = muse_call_output_path
    df['muse_sump_output'] = muse_sump_output_path
    unique_key_dict = {'uuid': uuid, 'muse_call_output': muse_call_output_path, 'muse_sump_output': muse_sump_output_path}
    table_name = 'time_mem_MuSE_sump_wgs'
    df_util.save_df_to_sqlalchemy(df, unique_key_dict, table_name, engine, logger)
    pipe_util.create_already_step(step_dir, sample_base + '_MuSE_sump', logger)
    logger.info('completed running `MuSE sump` of the tumor bam: %s' % input_name)
  return muse_sump_output_path