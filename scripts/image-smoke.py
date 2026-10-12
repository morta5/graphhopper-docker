import json
import argparse
from pathlib import Path
import tempfile
import secrets
import subprocess
import time
import urllib.request
parser = argparse.ArgumentParser(description='Autofahrt mit synthetischen Straßen im fertigen GraphHopper prüfen')
parser.add_argument('--image', required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
settings = tempfile.TemporaryDirectory(prefix='graphhopper-config-')
config = Path(settings.name)/'config.yml'
config.write_text((root/'config.yml').read_text().replace('/data/region.osm.pbf','/data/fixture.osm'))
name = 'graphhopper-image-proof-' + secrets.token_hex(6)
volume = name + '-data'
try:
    subprocess.run(['docker','volume','create',volume],capture_output=True,check=True)
    subprocess.run(['docker','run','--rm','--entrypoint','sh','-v',volume+':/data',
        '-v',str(root/'tests/fixtures/staging-roads.osm')+':/fixture.osm:ro',args.image,
        '-c','cat /fixture.osm > /data/fixture.osm'],capture_output=True,check=True)
    subprocess.run(['docker','run','-d','--name',name,'--cap-drop=ALL','--security-opt=no-new-privileges',
        '-v',volume+':/data','-v',str(config)+':/graphhopper/config.yml:ro','-p','127.0.0.1::8989',args.image],capture_output=True,check=True)
    address=subprocess.check_output(['docker','port',name,'8989/tcp'],text=True).strip()
    for attempt in range(90):
        try:
            with urllib.request.urlopen('http://'+address+'/route?point=54,10&point=54.001,10.001&profile=car',timeout=3) as response:
                data=json.load(response)
                assert response.status==200 and data['paths'][0]['distance']>0
            break
        except Exception:
            if attempt==89:
                logs=subprocess.run(['docker','logs','--tail','35',name],capture_output=True,text=True)
                print(logs.stdout,logs.stderr)
                raise RuntimeError('GraphHopper wird nicht routingbereit') from None
            time.sleep(.5)
    assert subprocess.check_output(['docker','exec',name,'id','-u'],text=True).strip()!='0'
    print('GraphHopper: echte Autofahrt auf synthetischen OSM-Straßen und unprivilegierte Laufzeit bestätigt')
finally:
    subprocess.run(['docker','rm','-f',name],capture_output=True)
    subprocess.run(['docker','volume','rm',volume],capture_output=True)
    settings.cleanup()
