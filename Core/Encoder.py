import marshal
import sys
import dis
import secrets
import os
import types

WORKING_DIR = "out"
class PYC_Struct:
    def __init__(self, header, payload) -> None:
        self.code_obj = payload
        self.header = header

def process_bytecode(path : str) -> PYC_Struct:
    header_size = 8
    if sys.version_info >= (3, 6):
        header_size = 12
    if sys.version_info >= (3, 7):
        header_size = 16
    with open(path, "rb") as f:
        metadata = f.read(header_size)
        code_obj = marshal.load(f)
    
    return PYC_Struct(metadata, code_obj)

class VM:
    def unpack_bytecode(self): 
        bytecode = self.pyc_struct.code_obj.co_code
        # FORMAT: OP_CODE OP_ARG (1 byte each)
        for i in range(0, len(bytecode), 2):
            opcode = bytecode[i]
            if opcode >= dis.HAVE_ARGUMENT:
                oparg = bytecode[i+1]
            else:
                oparg = None
            yield (i, opcode, oparg)

    
    def pack_bytecode(self,  enc_code : list):
        bytecode = bytearray()
        for _, opcode, oparg in enc_code:
            bytecode.append(opcode)
            if opcode >= dis.HAVE_ARGUMENT:
                bytecode.append(oparg)
            else:
                bytecode.append(0)
        self.packed_bytecode = bytes(bytecode)
        

    def create_vm_data(self):
        print("[+] Creating VM data")
        data : list = []
        self.enc_code = self.encrypt_bytecode(
            data,
            self.unpack_bytecode()
        )

        print(" - [=] Saving data...")
        with open(f'{WORKING_DIR}/vm_data', 'wb') as f:
            f.write(
                marshal.dumps(data)
            )

        
    def encrypt_bytecode(self, data : list, bytecode_data) -> list:
        print(" - [=] Encrypting bytecode...")
        res : list = []
        for i, opcode, oparg in bytecode_data:
            if oparg is not None:
                key = secrets.randbits(8)
                data.append(oparg ^ key)
                res.append((i, opcode, key))
            else:
                res.append((i, opcode, None))
        return res
    


    def write_vm_bytecode(self):
        print("[+] Saving virtual bytecode")
        code_obj : types.CodeType = self.pyc_struct.code_obj
        code_obj = code_obj.replace(
            co_code=self.packed_bytecode
        )

        # Write the modified bytecode to a file
        with open(f'{WORKING_DIR}/_m.vyc', 'wb') as f:
            f.write(self.pyc_struct.header)
            f.write(marshal.dumps(code_obj))


        
    def init(self):
        print("[+] Initializing environment")
        if not os.path.exists(WORKING_DIR):
            os.mkdir(WORKING_DIR)
    


    def __init__(self, pyc_struct : PYC_Struct) -> None:
        self.pyc_struct = pyc_struct
        self.init()
        self.create_vm_data()
        self.pack_bytecode(self.enc_code)
        self.write_vm_bytecode()
        print("[+] Done !")
        

            

        
    