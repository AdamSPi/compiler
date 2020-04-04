.section    __TEXT,__text
.globl _main

_start:
pushq %rbp
movq %rsp, %rbp
subq $32, %rsp
jmp _body

_body:
movq $3, -8(%rbp)
addq $2, -8(%rbp)
callq _read_int
movq %rax, -16(%rbp)
movq -16(%rbp), %rax
movq %rax, -24(%rbp)
movq -16(%rbp), %rax
addq %rax, -24(%rbp)
movq -24(%rbp), %rax
movq %rax, -32(%rbp)
movq -8(%rbp), %rax
addq %rax, -32(%rbp)
movq -32(%rbp), %rax
jmp _end

_end:
addq $32, %rsp
popq %rbp
retq

_main:
pushq %rbp
movq %rsp, %rbp
callq _start
movq %rax, %rdi
callq _print_int
popq %rbp
retq
