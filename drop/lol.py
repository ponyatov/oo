# lol.VM metaprogram: a sample of managed compilation in Python
 
# https://eli.thegreenplace.net/2015/building-and-using-llvmlite-a-basic-example/
 
import llvmlite.ir as ir
# lol: Virtual FORTH Machine (LLVM portable)
module = ir.Module('lol')
print module
 
# # import llvmlite.binding as llvm
# # 
# # llvm.initialize()
# # llvm.initialize_native_target()
# # llvm.initialize_native_asmprinter()
#  
# 
# # # llvm_module = llvm.parse_assembly(str(module)) ; print llvm_module
# # 
# # func_ty = ll.FunctionType(ll.IntType(32), [ll.IntType(32)])# , ll.IntType(32)])
# # func = ll.Function(module, func_ty, name='main')
# # 
# # func.args[0].name = 'argc'
# # # func.args[1].name = 'argv'
# 
# # type
# int32 = ir.IntType(32) ; print 'int32',int32
# int32p = ir.PointerType(int32)
# void = ir.VoidType
# char = ir.IntType(8);           # char = int8
# charp = ir.PointerType(char)    # *char
# charpp = ir.PointerType(charp)  # *char[]
# intfn = ir.FunctionType(int32,(int32p,charpp)) ; print 'intfn',intfn
#  
# main = ir.Function(module,intfn,name='main') ; print 'main',main
# 
# block = main.append_basic_block('entry') ; print block
# 
# builder = ir.IRBuilder(block)
# builder.ret()
#  
# print module
