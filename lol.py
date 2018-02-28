# lol.VM metaprogram: a sample of managed compilation in Python

# https://eli.thegreenplace.net/2015/building-and-using-llvmlite-a-basic-example/

import llvmlite.ir as ll
module = ll.Module('lol') # lol: Virtual FORTH Machine (LLVM portable assembler
print module

# import llvmlite.binding as llvm
# 
# llvm.initialize()
# llvm.initialize_native_target()
# llvm.initialize_native_asmprinter()
 

# # llvm_module = llvm.parse_assembly(str(module)) ; print llvm_module
# 
# func_ty = ll.FunctionType(ll.IntType(32), [ll.IntType(32)])# , ll.IntType(32)])
# func = ll.Function(module, func_ty, name='main')
# 
# func.args[0].name = 'argc'
# # func.args[1].name = 'argv'

print module
