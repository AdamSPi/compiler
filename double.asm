.section    __TEXT,__text
.globl _main
_main:
movq $5, %rax
addq %rax, %rax
retq
