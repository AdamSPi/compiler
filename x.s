.data
.text
.globl _main

_start:
pushq %rbp
movq %rsp, %rbp
subq $16, %rsp
jmp _body

_body:
callq _read_int
movq %rax, -8(%rbp)
movq -8(%rbp), %r13
addq $212, %r13
negq %r13
callq _read_int
movq %r13, %rbx
addq %rax, %rbx
negq %rbx
addq %r13, %rbx
callq _read_int
movq %rax, %r12
addq %r13, %r13
callq _read_int
addq %rax, %r13
negq %r13
movq %r13, %rax
addq %r12, %rax
addq %rbx, %rax
movq %rax, -16(%rbp)
negq -16(%rbp)
movq -16(%rbp), %rax
jmp _end

_end:
addq $16, %rsp
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
