.data
.text
.globl _main

_start:
pushq %rbp
movq %rsp, %rbp
pushq %r12
pushq %r13
pushq %r14
pushq %r15
subq $16, %rsp
jmp _body

_body:
callq _read_int
movq %rax, -8(%rbp)
movq -8(%rbp), %rcx
addq $-227, %rcx
movq %rcx, %rbx
addq %rcx, %rbx
negq %rbx
addq %rbx, %rcx
movq %rcx, %r12
negq %r12
callq _read_int
movq %rax, %r13
callq _read_int
addq %r13, %rax
movq $-217, %rbx
addq %rax, %rbx
addq %r12, %rbx
movq %rbx, -16(%rbp)
negq -16(%rbp)
movq -16(%rbp), %rax
jmp _end

_end:
addq $16, %rsp
popq %r15
popq %r14
popq %r13
popq %r12
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
