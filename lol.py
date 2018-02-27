# lol.VM metaprogram: a sample of managed compilation in Python

# https://eli.thegreenplace.net/2015/building-and-using-llvmlite-a-basic-example/

import llvmlite.ir as ll
import llvmlite.binding as llvm

llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

module = ll.Module('lol: Virtual FORTH Machine') #; print module
# llvm_module = llvm.parse_assembly(str(module)) ; print llvm_module

func_ty = ll.FunctionType(ll.IntType(32), [ll.IntType(32)])# , ll.IntType(32)])
func = ll.Function(module, func_ty, name='main')

func.args[0].name = 'argc'
# func.args[1].name = 'argv'

print module
