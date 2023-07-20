# MartyVM 🧬

**MartyVM** is a Python obfuscator capable of encrypting code at bytecode level.


## Why 💡

I wanted to do this project as a sort of proof of concept because I have never seen such program. It was also a way to put in practice the things I learned while researching about the Python bytecode.

## Disclaimer ⚠

If you want to use this code in a commercial software, you need to read and respect the **license**.


## Under the hood ⚙

### Virtualization

The "Virtual Machine" (not really one but rather a simple bytecode encryption program) takes a compile python script (.pyc) and extract the bytecode. Once the bytecode is extracted, we "encrypt" (XOR) each operand with a random key, the operand is now set to the key and all of the XORed operands are now stored inside a binary file ``vm_data`` . Finally we recompile the bytecode and save it as ``_m.vyc``.

### Runtime

At runtime, the program will again load ``vm_data`` and ``_m.vyc`` to decrypt the bytecode. Once the original code has been restored, a dynamic module containing the bytecode will be created and then ran.



## Usage
Before doing anything, you need to wrap your script code like such:
```python
def main():
  print('Hello, Marty !')

def entry_point():
  main()

```

Once the previous step is complete, compile your code:
```
py -m compileall file.py
```

Next, run Marty 
```
py marty.py file_compiled.pyc
```

Marty will write file needed for the runtime inside ``*/out/``. Navigate here and make sure that ``runtime.py`` is also located here, finally run your program by using:
```
py runtime.py
```


## Room for improvement

I have multiple ideas in mind to improve this project:

- Alter the opcodes or/and add custom ones
- Improve encryption on arguments
- Improve runtime, the code is the most vulnerable at runtime, a simple hook on the "exec" method could expose the decrypted bytecode to an attacker. A solution could be to create a native library to handle the runtime (planned).
