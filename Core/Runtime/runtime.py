import dis
import sys
import marshal
import importlib.util
class Runtime:
    def load_vm_data(self):
        with open('vm_data', 'rb') as f:
            self.vm_data = marshal.loads(
                f.read()
            )

    def decrypt(self):
        res = []
        y = 0
        bytecode = self.code_obj.co_code
        for i in range(0, len(bytecode), 2):
            opcode = bytecode[i]
            if opcode >= dis.HAVE_ARGUMENT:
                oparg = bytecode[i+1] ^ self.vm_data[y]
                y += 1
            else:
                oparg = None

            res.append((opcode, oparg))
        return res

    def run(self):
        module_name = ''
        module_spec = importlib.util.spec_from_loader(module_name, loader=None)
        dynamic_module = importlib.util.module_from_spec(module_spec)
        dynamic_module.__dict__.update({'__name__': module_name})
        exec(self.code_obj, dynamic_module.__dict__)
        dynamic_module.entry_point()

    
    def pack_bytecode(self,  enc_code : list):
        bytecode = bytearray()
        for ins in enc_code:
            opcode = ins[0]
            oparg = ins[1]
            bytecode.append(opcode)
            if opcode >= dis.HAVE_ARGUMENT:
                bytecode.append(oparg)
            else:
                bytecode.append(0)

        self.code_obj = self.code_obj.replace(
            co_code=bytes(bytecode)
        )


    def load_bytecode(self):
        header_size = 8
        if sys.version_info >= (3, 6):
            header_size = 12
        if sys.version_info >= (3, 7):
            header_size = 16
        with open('_m.vyc', "rb") as f:
            _ = f.read(header_size)
            code_obj = marshal.load(f)
    
        self.code_obj = code_obj


if __name__ == "__main__":
    rt = Runtime()
    rt.load_vm_data()
    rt.load_bytecode()
    rt.pack_bytecode(
        rt.decrypt()
    )
    rt.run()
    