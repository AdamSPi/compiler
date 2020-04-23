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
movq $175, %r12
addq %rax, %r12
callq _read_int
movq %rax, %rbx
addq %r12, %rbx
callq _read_int
movq %rax, %r12
negq %r12
addq %rbx, %r12
callq _read_int
movq %rax, %rbx
addq %r12, %rbx
negq %rbx
negq %rbx
negq %rbx
callq _read_int
movq %rax, %r12
negq %r12
movq $-95, %r13
addq %r12, %r13
callq _read_int
addq %rax, %r12
addq %r13, %r12
callq _read_int
addq $-528, %rax
addq %r12, %rax
addq $-36, %rax
addq %rbx, %rax
movq %rax, -8(%rbp)
negq -8(%rbp)
movq -8(%rbp), %rax
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
