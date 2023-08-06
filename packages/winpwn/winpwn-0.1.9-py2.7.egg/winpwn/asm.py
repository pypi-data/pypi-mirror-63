from .context import context

def disasm(machine_code,addr=0):
    import capstone
    disasmer=capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    if context.arch=="amd64":
        disasmer=capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    l=""
    for i in disasmer.disasm(machine_code,addr):
        l+="\t{:8s} {};\n".format(i.mnemonic,i.op_str)
    return l.strip('\n')

def asm(asm_code,addr=0):
    import keystone
    asmer=keystone.Ks(keystone.KS_ARCH_X86,keystone.KS_MODE_32)
    if context.arch=="amd64":
        asmer=keystone.Ks(keystone.KS_ARCH_X86,keystone.KS_MODE_64)
    l=""
    for i in asmer.asm(asm_code,addr)[0]:
        l+=chr(i)
    return l


