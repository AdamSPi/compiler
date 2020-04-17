.data
.text
.globl _main

_start:
pushq %rbp
movq %rsp, %rbp
subq $48, %rsp
jmp _body

_body:
callq _read_int
movq %rax, -8(%rbp)
movq -8(%rbp), %rax
movq %rax, -16(%rbp)
addq $355, -16(%rbp)
movq -16(%rbp), %rax
movq %rax, -24(%rbp)
negq -24(%rbp)
movq $-2, -32(%rbp)
movq -24(%rbp), %rax
addq %rax, -32(%rbp)
movq -32(%rbp), %rax
movq %rax, -40(%rbp)
negq -40(%rbp)
movq -40(%rbp), %rax
jmp _end

_end:
addq $48, %rsp
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
