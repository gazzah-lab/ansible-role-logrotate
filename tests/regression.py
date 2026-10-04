import json, os, subprocess
from pathlib import Path

def run(role, variables, tags=None, success=True):
 cmd=['ansible-playbook','-i','localhost,','-c','local',str(Path(__file__).with_name('test.yml')),'-e',json.dumps(variables)]
 if tags: cmd+=['--tags',tags]
 result=subprocess.run(cmd,capture_output=True,text=True)
 if (result.returncode==0)!=success: raise AssertionError(result.stdout+result.stderr)
 print(role,tags or 'all','PASS',flush=True)
for name, folder, marker, key, valid in [
 ('cron','/etc/cron.d','gazzah.cron','cron_jobs',[{'name':'check','cron_file':'example','user':'aymen.gazzah','job':'/usr/bin/true','disabled':True}]),
 ('logrotate','/etc/logrotate.d','gazzah.logrotate','logrotate_configs',[{'name':'example','paths':['/var/log/example/*.log'],'options':['missingok','daily','rotate 7']}])]:
 if name != 'logrotate': continue
 p=Path(folder); foreign=p/'foreign_test'; orphan=p/'owned_orphan'
 foreign.write_text('# external configuration\n')
 orphan.write_text(f'# ANSIBLE MANAGED - {marker}\n')
 run(name,{key:[]},f'{name}-cleanup',False)
 assert orphan.exists() and foreign.read_text()=='# external configuration\n'
 run(name,{key:valid})
 assert not orphan.exists() and foreign.read_text()=='# external configuration\n'
 if name=='cron': assert '#* * * * * aymen.gazzah /usr/bin/true' in (p/'example').read_text()
 else:
  before=(p/'example').read_text()
  run(name,{key:[{'name':'example','paths':['/var/log/example/*.log'],'options':['this_is_invalid']} ]},success=False)
  assert (p/'example').read_text()==before
 foreign.unlink()
