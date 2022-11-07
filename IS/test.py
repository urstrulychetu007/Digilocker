from ethairballoons.ethairballoons import ethairBalloons
from glob import glob
import json
prov = ethairBalloons('127.0.0.1', '..')


def digilocker(id,filename):
    data = json.loads((docSchema.findById(id)))
    if filename == 'A':
        return data['aadharval']
    return data['clgidval']




docSchema = prov.createSchema(modelDefinition={
    'name': "Documents",
    'contractName': "docsContract",
    'properties': [{
            'name': "id",
            'type': "bytes32",
            'primaryKey': True
    },
       
        {
            'name': "aadharval",
            'type': "bytes32"
    },
    
     {
            'name': "clgidval",
            'type': "bytes32"
    }
    ]
})
docSchema.deploy()

aadhar_files = glob('/home/chetan/Documents/7th Sem/IS/static/aadhaar/images/*.txt')

for i in aadhar_files:
    data = open(i,'r')
    clgfile = open('/home/chetan/Documents/7th Sem/IS/static/collegeid/images/'+i.split('/')[-1],'r')
    clgval = clgfile.read()
    data=data.read()
    receipt = docSchema.save({
        'id':i.split('/')[-1][:-4],
        'aadharval':i.split('/')[-1],
        'clgidval': i.split('/')[-1]
    })
    # print(receipt)

